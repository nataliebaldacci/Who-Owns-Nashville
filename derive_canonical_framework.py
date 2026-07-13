"""Materialize the canonical U1 framework parquet from the existing baseline.

Applies the FULL canonical where-clause (all three conditions) to
Nashville_Framework_Homes_BASELINE and recomputes the owner split with the
FIXED canonical classifier (post 2026-07-13 reconciliation).

RUN (copy-paste, no edits):

    cd /Users/nataliebaldacci/Master_Data/Nashville/Key_datasets
    python3 derive_canonical_framework.py Nashville_Framework_Homes_BASELINE_2026-07-07.parquet

Writes:
    Nashville_Framework_Homes_CANONICAL_2026-07-07.parquet   (the U1 file of record)
and prints the counts to paste back. Expected ~206,067 rows (county query said
205,933 on July 6; the ~134 difference is one-day snapshot drift).
"""
import sys, os

USE_LIST = {"NULL", "SINGLE FAMILY", "ZERO LOT LINE", "DUPLEX", "RESIDENTIAL CONDO"}
FEATURE_EXCL = {"MULTISTORY CONDO", "MULTISTORY COMMON AREA", "OPEN SPACE"}

# fixed canonical M1 classifier (canonical_universes.py, 2026-07-13)
ENTITY_TOKENS = ["LLC", "LLP", " LP", "L.P", " INC", "CORP", "LTD", "LIMITED",
                 " CO ", "CO.", "COMPANY", "PARTNER", "ASSOC", "HOMES", "HOLDING",
                 "CAPITAL", "INVEST", "FUND", "SOLUTION", "SFR", "ASSET", "BORROW", " JV"]
GOVERNMENT_TOKENS = ["CITY OF", "HOUSING AUTH", "STATE OF", "COUNTY OF", " HUD ",
                     "MDHA", "UNITED STATES", "METROPOLITAN GOV", "METRO GOV",
                     "SECRETARY OF", "VETERANS AFFAIRS"]
TRUST_TOKENS = ["TRUST", "TRUSTEE", "REVOCABLE", "LIVING TR", "FAMILY TR",
                " TR ", "COMMUNITY PROPERTY"]
BANK_TOKENS = [" BANK ", "MORTGAGE", "LENDER", "FEDERAL NATIONAL", "FANNIE MAE",
               "FREDDIE MAC", "FEDERAL HOME LOAN"]


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


def find_col(cols, *cands):
    low = {c.lower(): c for c in cols}
    for cand in cands:
        if cand.lower() in low: return low[cand.lower()]
    for cand in cands:
        for c in cols:
            if cand.lower() in c.lower(): return c
    return None


def main(path):
    import pandas as pd
    df = pd.read_parquet(path)
    col_du = find_col(df.columns, "Current_DUCOUNT", "ducount")
    col_ft = find_col(df.columns, "Current_FeatureType", "featuretype")
    col_lu = find_col(df.columns, "Current_LUDESC", "ludesc")
    col_nm = find_col(df.columns, "owner_name_dedup", "Current_Owner", "owner_name", "owner")

    du = pd.to_numeric(df[col_du], errors="coerce")
    ft = df[col_ft].astype(str).str.strip().str.upper()
    lu = df[col_lu].astype(str).str.strip().str.upper()
    keep = du.isin([1, 2]) & lu.isin(USE_LIST) & ~ft.isin(FEATURE_EXCL)
    canon = df[keep].copy()
    print(f"baseline {len(df):,} -> canonical U1 {len(canon):,}  "
          f"(county July-6 query: 205,933; expected drift ~ +134)")
    print("\nland-use mix:")
    print(canon[col_lu].astype(str).str.upper().value_counts().to_string())

    # canonical owner split with the FIXED classifier
    names = canon[col_nm].astype(str).str.upper()
    uniq = names.drop_duplicates()
    print(f"\nclassifying {len(uniq):,} unique owner names (fixed canonical M1) ...")
    canon["owner_type_canonical"] = names.map({nm: classify_owner(nm) for nm in uniq})
    print(canon["owner_type_canonical"].value_counts().to_string())
    print("\n(funnel published: Individual 172,407 / Entity 16,769 / Trust 16,188 / "
          "Bank-Lender 161 / Government 408)")

    out = path.replace("BASELINE", "CANONICAL")
    if out == path:
        out = os.path.splitext(path)[0] + "_CANONICAL.parquet"
    canon.to_parquet(out, index=False)
    print(f"\nwrote {out}  ({os.path.getsize(out)/1e6:,.1f} MB)")
    print(">>> Paste this output back into the chat.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: python3 derive_canonical_framework.py <baseline.parquet>")
    main(sys.argv[1])
