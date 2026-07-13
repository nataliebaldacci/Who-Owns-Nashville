"""Close the last two gaps in the baseline reconciliation: the +1,467 row
residual and the owner-classifier drift. Print-only; paste the output back.

RUN (copy-paste, no edits):

    cd /Users/nataliebaldacci/Master_Data/Nashville/Key_datasets
    python3 baseline_residual_check.py Nashville_Framework_Homes_BASELINE_2026-07-07.parquet
"""
import sys

FEATURE_EXCL = {"MULTISTORY CONDO", "MULTISTORY COMMON AREA", "OPEN SPACE"}

# canonical M1 classifier (inlined from canonical_universes.py)
ENTITY_TOKENS = ["LLC", "LLP", " LP", "L.P", " INC", "CORP", "LTD", "LIMITED",
                 " CO ", "CO.", "COMPANY", "PARTNER", "ASSOC", "HOMES", "HOLDING",
                 "CAPITAL", "INVEST", "FUND", "SOLUTION", "SFR", "ASSET", "BORROW", " JV"]
GOVERNMENT_TOKENS = ["CITY OF", "HOUSING AUTH", "STATE OF", "COUNTY OF", "HUD",
                     "MDHA", "UNITED STATES", "METROPOLITAN GOV", "METRO GOV"]
TRUST_TOKENS = ["TRUST", "REVOCABLE", "LIVING TR", "FAMILY TR"]
BANK_TOKENS = ["BANK", "MORTGAGE", "LENDER", "FEDERAL NATIONAL", "FANNIE MAE",
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
    col_ot = find_col(df.columns, "owner_type", "owner_category")
    col_apn = find_col(df.columns, "APN", "ParID", "parcel_id", "parcelid", "pin")
    col_nm = find_col(df.columns, "Current_Owner", "OwnName", "owner_name", "owner")
    print("columns ->", dict(du=col_du, ft=col_ft, lu=col_lu, owner_type=col_ot,
                             apn=col_apn, owner_name=col_nm))

    du = pd.to_numeric(df[col_du], errors="coerce")
    ft = df[col_ft].astype(str).str.strip().str.upper()
    keep = du.isin([1, 2]) & ~ft.isin(FEATURE_EXCL)
    k = df[keep]
    print(f"\nkept: {len(k):,}  (county target 205,933, residual {len(k)-205933:+,})")

    # --- residual check 1: LUDESC null vs literal 'NULL'
    lu_raw = k[col_lu]
    print("\n[LUDESC in kept set]")
    print("  literal string 'NULL':", int((lu_raw.astype(str).str.strip().str.upper() == "NULL").sum()))
    print("  actual null/NaN:      ", int(lu_raw.isna().sum()))
    print("  empty string:         ", int((lu_raw.astype(str).str.strip() == "").sum()))
    print("  top values:")
    print(lu_raw.astype(str).str.upper().value_counts().head(8).to_string())

    # --- residual check 2: duplicate parcels
    if col_apn:
        dups = int(k[col_apn].duplicated().sum())
        print(f"\n[duplicates] repeated {col_apn} rows in kept set: {dups:,}")

    # --- classifier drift: canonical vs file owner_type on the kept set
    if col_nm and col_ot:
        names = k[col_nm].astype(str).str.upper()
        uniq = names.drop_duplicates()
        print(f"\n[classifier] classifying {len(uniq):,} unique names ...")
        cls = names.map({nm: classify_owner(nm) for nm in uniq})
        ct = pd.crosstab(cls.rename("canonical"), k[col_ot].astype(str).rename("file_owner_type"))
        print(ct.to_string())
        print("\ncanonical totals on kept set:")
        print(cls.value_counts().to_string())
        # examples of the biggest disagreement cells
        both = pd.DataFrame({"canonical": cls, "file": k[col_ot].astype(str), "name": names})
        dis = both[both["canonical"] != both["file"].replace(
            {"Corporate": "Entity", "Bank/Lender": "Bank-Lender"})]
        print(f"\ndisagreements: {len(dis):,} rows. Examples by cell:")
        for (a, b), grp in dis.groupby(["canonical", "file"]):
            ex = grp["name"].drop_duplicates().head(3).tolist()
            print(f"  canonical={a:12} file={b:12} n={len(grp):>6,}  e.g. {ex}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: python3 baseline_residual_check.py <baseline.parquet>")
    main(sys.argv[1])
