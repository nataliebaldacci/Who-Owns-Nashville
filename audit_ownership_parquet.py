"""Audit the enriched Ownership History parquet against the canonical universe
spec (UNIVERSE.md), entirely on your machine. Self-contained: no other repo
files needed.

RUN (copy-paste, no edits needed):

    cd ~/Master_Data/Nashville/Key_datasets
    python3 audit_ownership_parquet.py Ownership_History_Enriched_Cleaned_2026-07-11_txntier.parquet

It prints the audit and writes two SMALL files next to the parquet:
    parquet_audit_summary.json   (schema, counts, spec checks)  ~ a few KB
    parquet_sample_5k.csv        (5,000-row random sample)      ~ 1-2 MB
Upload those two files back into the chat.

Needs: pandas + pyarrow  (pip3 install pandas pyarrow  if missing).
"""
import sys, os, json, random

# ---------- canonical measures (inlined from canonical_universes.py) ----------
ENTITY_TOKENS = ["LLC", "LLP", " LP", "L.P", " INC", "CORP", "LTD", "LIMITED",
                 " CO ", "CO.", "COMPANY", "PARTNER", "ASSOC", "HOMES", "HOLDING",
                 "CAPITAL", "INVEST", "FUND", "SOLUTION", "SFR", "ASSET", "BORROW", " JV"]
GOVERNMENT_TOKENS = ["CITY OF", "HOUSING AUTH", "STATE OF", "COUNTY OF", "HUD",
                     "MDHA", "UNITED STATES", "METROPOLITAN GOV", "METRO GOV"]
TRUST_TOKENS = ["TRUST", "REVOCABLE", "LIVING TR", "FAMILY TR"]
BANK_TOKENS = ["BANK", "MORTGAGE", "LENDER", "FEDERAL NATIONAL", "FANNIE MAE",
               "FREDDIE MAC", "FEDERAL HOME LOAN"]
DAVIDSON_ZIPS = {"37013", "37072", "37076", "37080", "37115", "37138", "37189",
                 "37228"} | {f"372{i:02d}" for i in range(1, 22)}
EXPECTED = {"deed_events": 1_641_434, "deed_events_corporate": 199_158}


def _norm(name):
    out = "".join(c if c.isalnum() or c == "." else " " for c in str(name or "").upper())
    return f" {' '.join(out.split())} "


def classify_owner(name):
    n = _norm(name)
    if any(t in n for t in GOVERNMENT_TOKENS): return "Government"
    if any(t in n for t in TRUST_TOKENS):      return "Trust"
    if any(t in n for t in BANK_TOKENS):       return "Bank-Lender"
    if any(t in n for t in ENTITY_TOKENS):     return "Entity"
    return "Individual"


# ------------------------------- audit ---------------------------------------
def find_col(cols, *cands):
    """Fuzzy column finder: exact (case-insensitive) then substring."""
    low = {c.lower(): c for c in cols}
    for cand in cands:
        if cand.lower() in low:
            return low[cand.lower()]
    for cand in cands:
        for c in cols:
            if cand.lower() in c.lower():
                return c
    return None


def main(path):
    import pandas as pd
    print(f"file: {path}  ({os.path.getsize(path)/1e6:,.1f} MB)")
    df = pd.read_parquet(path)
    n = len(df)
    print(f"rows: {n:,}   cols: {len(df.columns)}")
    print("schema:")
    for c, t in df.dtypes.items():
        print(f"   {c:28} {t}")

    summary = {"file": os.path.basename(path), "rows": n,
               "columns": {c: str(t) for c, t in df.dtypes.items()},
               "checks": {}, "value_counts": {}}

    # locate key columns flexibly
    col_owner = find_col(df.columns, "OwnName", "owner_name", "owner", "name", "grantee")
    col_state = find_col(df.columns, "StateCode", "own_state", "state")
    col_ozip  = find_col(df.columns, "OwnZip", "owner_zip", "mail_zip", "ownerzip", "zip_owner")
    col_pzip  = find_col(df.columns, "PropZip", "parcel_zip", "prop_zip", "situs_zip")
    col_tier  = find_col(df.columns, "txntier", "tier")
    col_year  = find_col(df.columns, "AcqDate", "acq_year", "year", "date")
    col_class = find_col(df.columns, "owner_class", "owner_type", "entity_flag", "is_entity", "class")
    print("\nkey columns ->", dict(owner=col_owner, state=col_state, owner_zip=col_ozip,
                                   parcel_zip=col_pzip, txntier=col_tier, date=col_year,
                                   precomputed_class=col_class))

    # --- U3 check 1: total events vs spec
    summary["checks"]["total_vs_expected_1641434"] = {"rows": n, "expected": EXPECTED["deed_events"],
                                                      "delta": n - EXPECTED["deed_events"]}
    print(f"\n[U3] total events: {n:,}  (spec 1,641,434, delta {n-EXPECTED['deed_events']:+,})")

    # --- txntier distribution
    if col_tier:
        vc = df[col_tier].astype(str).value_counts()
        summary["value_counts"]["txntier"] = vc.to_dict()
        print("\n[txntier] distribution:")
        print(vc.to_string())

    # --- M1: corporate test vs spec (sampled for speed if huge, full if feasible)
    if col_owner:
        names = df[col_owner]
        uniq = names.astype(str).str.upper().drop_duplicates()
        print(f"\n[M1] unique owner names: {len(uniq):,} — classifying (may take ~1-2 min)")
        cls_map = {nm: classify_owner(nm) for nm in uniq}
        cls = names.astype(str).str.upper().map(cls_map)
        vc = cls.value_counts()
        summary["value_counts"]["owner_class_canonical"] = vc.to_dict()
        corp = int(vc.get("Entity", 0))
        summary["checks"]["corporate_vs_expected_199158"] = {"entity_events": corp,
            "expected": EXPECTED["deed_events_corporate"], "delta": corp - EXPECTED["deed_events_corporate"]}
        print(vc.to_string())
        print(f"[M1] entity deed events: {corp:,}  (spec 199,158, delta {corp-EXPECTED['deed_events_corporate']:+,})")
        # agreement with any precomputed class column
        if col_class:
            both = pd.crosstab(cls, df[col_class].astype(str))
            summary["checks"]["canonical_vs_precomputed_crosstab"] = both.to_dict()
            print("\n[M1] canonical classifier vs file's own class column:")
            print(both.to_string())

    # --- M2: zip match / out-of-state
    if col_ozip and col_pzip:
        oz = df[col_ozip].astype(str).str[:5]
        pz = df[col_pzip].astype(str).str[:5]
        match = (oz == pz) & (oz != "") & (oz.str.lower() != "nan")
        ooc = ~oz.isin(DAVIDSON_ZIPS)
        summary["checks"]["zip_match_owner_occupied_events"] = int(match.sum())
        summary["checks"]["out_of_county_events"] = int(ooc.sum())
        print(f"\n[M2] ZIP-match (owner-occ proxy): {int(match.sum()):,} of {n:,}")
        print(f"[M2] out-of-county mailing ZIP:   {int(ooc.sum()):,}")
    if col_state:
        oos = (df[col_state].astype(str).str.strip().str.upper() != "TN")
        summary["checks"]["out_of_state_events"] = int(oos.sum())
        print(f"[M2] out-of-state (State<>TN):    {int(oos.sum()):,}  (spec cites 126,649 OOS deed records)")

    # --- outputs
    out_dir = os.path.dirname(os.path.abspath(path))
    jpath = os.path.join(out_dir, "parquet_audit_summary.json")
    json.dump(summary, open(jpath, "w"), indent=1, default=str)
    spath = os.path.join(out_dir, "parquet_sample_5k.csv")
    df.sample(n=min(5000, n), random_state=42).to_csv(spath, index=False)
    print(f"\nwrote {jpath}")
    print(f"wrote {spath}  ({os.path.getsize(spath)/1e6:,.1f} MB)")
    print("\n>>> Upload parquet_audit_summary.json and parquet_sample_5k.csv back into the chat.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: python3 audit_ownership_parquet.py <path-to-parquet>")
    main(sys.argv[1])
