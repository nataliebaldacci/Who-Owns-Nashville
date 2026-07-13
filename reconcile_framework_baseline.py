"""Reconcile Nashville_Framework_Homes_BASELINE (225,471 rows) against the
canonical U1 framework (205,933). Applies the two missing filter conditions
(DUCOUNT in 1,2 + FeatureType exclusions) locally and reports what drops.

RUN (copy-paste, no edits):

    cd /Users/nataliebaldacci/Master_Data/Nashville/Key_datasets
    python3 reconcile_framework_baseline.py Nashville_Framework_Homes_BASELINE_2026-07-07.parquet

Writes: baseline_reconciliation.json  (small — upload it back into the chat)

Needs: pandas + pyarrow.
"""
import sys, os, json

TARGET = 205_933
FEATURE_EXCL = {"MULTISTORY CONDO", "MULTISTORY COMMON AREA", "OPEN SPACE"}
FUNNEL_SPLIT = {"Individual": 172_407, "Entity": 16_769, "Trust": 16_188,
                "Bank-Lender": 161, "Government": 408}


def find_col(cols, *cands):
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
    df = pd.read_parquet(path)
    n0 = len(df)
    print(f"rows: {n0:,}  (baseline; canonical target {TARGET:,})")

    col_du = find_col(df.columns, "Current_DUCount", "ducount", "du_count", "DUCount")
    col_ft = find_col(df.columns, "Current_FeatureType", "featuretype", "feature_type")
    col_lu = find_col(df.columns, "Current_LUDesc", "ludesc", "lu_desc", "landuse")
    col_ot = find_col(df.columns, "owner_type", "owner_category", "owner_class")
    print("columns ->", dict(ducount=col_du, featuretype=col_ft, ludesc=col_lu, owner_type=col_ot))
    out = {"rows_baseline": n0, "target": TARGET,
           "columns": dict(ducount=col_du, featuretype=col_ft, ludesc=col_lu, owner_type=col_ot)}

    if not col_du or not col_ft:
        out["error"] = "DUCount and/or FeatureType column not found - cannot re-derive locally"
        print(out["error"])
        print("available columns:")
        for c in df.columns: print("  ", c)
    else:
        du = pd.to_numeric(df[col_du], errors="coerce")
        ft = df[col_ft].astype(str).str.strip().str.upper()
        keep = du.isin([1, 2]) & ~ft.isin(FEATURE_EXCL)
        n1 = int(keep.sum())
        out["rows_after_missing_conditions"] = n1
        out["delta_vs_target"] = n1 - TARGET
        print(f"\nafter DUCOUNT in (1,2) AND FeatureType exclusions: {n1:,}  "
              f"(target {TARGET:,}, delta {n1-TARGET:+,})")

        # what drops, and why
        dropped = df[~keep]
        why = {}
        bad_du = int((~du.isin([1, 2])).sum())
        bad_ft = int(ft.isin(FEATURE_EXCL).sum())
        why["fails_ducount"] = bad_du
        why["fails_featuretype"] = bad_ft
        why["fails_both"] = int(((~du.isin([1, 2])) & ft.isin(FEATURE_EXCL)).sum())
        out["drop_reasons"] = why
        print(f"dropped {n0-n1:,}: ducount {bad_du:,} | featuretype {bad_ft:,} | both {why['fails_both']:,}")
        if col_lu:
            out["dropped_by_ludesc"] = dropped[col_lu].astype(str).value_counts().head(12).to_dict()
            print("\ndropped rows by land use:")
            print(dropped[col_lu].astype(str).value_counts().head(12).to_string())
        out["dropped_by_featuretype"] = dropped[col_ft].astype(str).value_counts().head(12).to_dict()

        # owner-type split, before vs after
        if col_ot:
            before = df[col_ot].astype(str).value_counts().to_dict()
            after = df.loc[keep, col_ot].astype(str).value_counts().to_dict()
            out["owner_split_baseline"] = before
            out["owner_split_after_filter"] = after
            out["owner_split_funnel_published"] = FUNNEL_SPLIT
            print("\nowner-type split baseline -> after filter (funnel target):")
            for k in sorted(set(before) | set(after)):
                print(f"   {k:15} {before.get(k,0):>9,} -> {after.get(k,0):>9,}")
            print("   funnel:", FUNNEL_SPLIT)

    jpath = os.path.join(os.path.dirname(os.path.abspath(path)), "baseline_reconciliation.json")
    json.dump(out, open(jpath, "w"), indent=1, default=str)
    print(f"\nwrote {jpath}")
    print(">>> Upload baseline_reconciliation.json into the chat.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: python3 reconcile_framework_baseline.py <baseline.parquet>")
    main(sys.argv[1])
