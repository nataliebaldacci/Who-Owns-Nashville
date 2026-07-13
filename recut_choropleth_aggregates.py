"""Re-cut the tract and block-group choropleth aggregates from the canonical U1
framework parquet, replacing the divergent legacy extracts (224,322 / 232,863
universes) with one reconciled cut.

RUN (copy-paste, no edits):

    cd /Users/nataliebaldacci/Master_Data/Nashville/Key_datasets
    python3 recut_choropleth_aggregates.py

It joins Nashville_Framework_Homes_CANONICAL_2026-07-07.parquet to
Regrid_Census_Geography_FIXED_2026-07-07.parquet on parcel id and writes two
SMALL files to upload back:

    choropleth_tract_canonical.csv        (~174 rows)
    choropleth_blockgroup_canonical.csv   (~487 rows)

Columns per geography: framework homes (denominator), entity-owned (M1),
trust-owned, out-of-state, and operator-attributed (M3) if an ultimate-parent
column exists. I regenerate the site GeoJSONs from these.
"""
import os, sys

CANON = "Nashville_Framework_Homes_CANONICAL_2026-07-07.parquet"
GEO = "Regrid_Census_Geography_FIXED_2026-07-07.parquet"


def find_col(cols, *cands):
    low = {c.lower(): c for c in cols}
    for cand in cands:
        if cand.lower() in low: return low[cand.lower()]
    for cand in cands:
        for c in cols:
            if cand.lower() in c.lower(): return c
    return None


def main():
    import pandas as pd
    k = pd.read_parquet(CANON)
    g = pd.read_parquet(GEO)
    print(f"canonical: {len(k):,} rows | geography: {len(g):,} rows")
    print("geography columns:", list(g.columns))

    kid = find_col(k.columns, "parcelid", "APN", "ParID", "pin")
    gid = find_col(g.columns, "parcelid", "APN", "ParID", "pin")
    tr = find_col(g.columns, "tract", "GEOID_tract", "tract_geoid", "census_tract")
    bg = find_col(g.columns, "blockgroup", "block_group", "GEOID_bg", "bg_geoid")
    ot = find_col(k.columns, "owner_type_canonical")
    up = find_col(k.columns, "owner_ultimate_parent", "ultimate_parent", "operator")
    st = find_col(k.columns, "owner_state", "StateCode", "own_state", "mail_state")
    print("join keys ->", dict(canon_id=kid, geo_id=gid, tract=tr, blockgroup=bg,
                               owner_type=ot, ultimate_parent=up, state=st))

    m = k.merge(g[[c for c in (gid, tr, bg) if c]], left_on=kid, right_on=gid, how="left")
    matched = m[tr].notna().sum() if tr else 0
    print(f"joined: {matched:,}/{len(k):,} parcels matched to a tract "
          f"({100*matched/len(k):.1f}%)")

    if up:
        print("\nultimate-parent sample (top 10):")
        print(m[up].astype(str).value_counts().head(10).to_string())

    def agg(level_col, out_name):
        d = m[m[level_col].notna()].copy()
        grp = d.groupby(d[level_col].astype(str))
        out = pd.DataFrame({
            "framework_n": grp.size(),
            "entity_n": grp.apply(lambda x: int((x[ot] == "Entity").sum())),
            "trust_n": grp.apply(lambda x: int((x[ot] == "Trust").sum())),
        })
        if st:
            out["oos_n"] = grp.apply(lambda x: int(
                (x[st].astype(str).str.strip().str.upper() != "TN").sum()))
        if up:
            attributed = d[up].astype(str).str.strip()
            d["_attr"] = attributed.ne("") & ~attributed.str.lower().isin(
                ["nan", "none", "other", "unattributed"])
            out["institutional_n"] = grp.apply(lambda x: int(d.loc[x.index, "_attr"].sum()))
        out["entity_pct"] = (100 * out["entity_n"] / out["framework_n"]).round(2)
        if "institutional_n" in out:
            out["institutional_pct"] = (100 * out["institutional_n"] / out["framework_n"]).round(2)
        out.index.name = level_col
        out.to_csv(out_name)
        print(f"\nwrote {out_name}  ({len(out)} geographies)")
        print(out.head(4).to_string())
        return out

    if tr:
        agg(tr, "choropleth_tract_canonical.csv")
    if bg:
        agg(bg, "choropleth_blockgroup_canonical.csv")
    print("\n>>> Upload the two CSVs into the chat.")


if __name__ == "__main__":
    for f in (CANON, GEO):
        if not os.path.exists(f):
            sys.exit(f"missing {f} - run from Key_datasets after derive_canonical_framework.py")
    main()
