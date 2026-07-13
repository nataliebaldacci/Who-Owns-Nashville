"""Re-run Part I's headline 1.47x burdened-tract concentration on the CANONICAL
framework. The master audit (2026-07-13) flags this as the project's single most
important open question: the 1.47x only reproduces on the deprecated 20,045
universe and has never been re-run on the correct framework.

RUN (copy-paste, no edits):

    cd /Users/nataliebaldacci/Master_Data/Nashville/Key_datasets
    python3 rerun_burdened_tract_finding.py

Needs, all in Key_datasets:
    Nashville_Framework_Homes_CANONICAL_2026-07-07.parquet
    Regrid_Census_Geography_FIXED_2026-07-07.parquet
    ACS_Housing_DP04_Tract_2011-2024.parquet

Computes, per tract: entity-owned rate (M1, canonical classifier) on the
framework universe, then the concentration ratio (mean rate in cost-burdened
tracts / countywide rate) under several burden definitions, since Part I's
exact threshold must be pinned. Prints everything; writes
burdened_tract_rerun.json to upload back.
"""
import os, sys, json

CANON = "Nashville_Framework_Homes_CANONICAL_2026-07-07.parquet"
GEO = "Regrid_Census_Geography_FIXED_2026-07-07.parquet"
ACS = "ACS_Housing_DP04_Tract_2011-2024.parquet"


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
    a = pd.read_parquet(ACS)
    print(f"canonical {len(k):,} | geography {len(g):,} | ACS tract rows {len(a):,}")
    print("ACS columns:", list(a.columns))

    kid = find_col(k.columns, "parcelid", "APN", "ParID")
    gid = find_col(g.columns, "parcelid", "APN", "ParID")
    tr = find_col(g.columns, "tract", "GEOID_tract", "tract_geoid", "census_tract")
    ot = find_col(k.columns, "owner_type_canonical")
    m = k.merge(g[[gid, tr]], left_on=kid, right_on=gid, how="left")
    m = m[m[tr].notna()].copy()
    m["_tract"] = m[tr].astype(str).str[-6:]        # last 6 = tract code within county
    print(f"parcels with tract: {len(m):,}")

    # per-tract framework counts + entity rate
    grp = m.groupby("_tract")
    t = pd.DataFrame({
        "framework_n": grp.size(),
        "entity_n": grp.apply(lambda x: int((x[ot] == "Entity").sum())),
    })
    t["entity_rate"] = 100 * t["entity_n"] / t["framework_n"]
    county_rate = 100 * (m[ot] == "Entity").sum() / len(m)
    print(f"\ncountywide entity rate on framework: {county_rate:.2f}%")

    # ACS: latest year, find tract id + cost-burden columns
    ay = find_col(a.columns, "year")
    if ay:
        a = a[a[ay] == a[ay].max()].copy()
        print(f"ACS year used: {a[ay].max()}")
    aid = find_col(a.columns, "GEOID", "tract", "geoid")
    burden_cols = [c for c in a.columns if any(t_ in c.lower() for t_ in
                   ("burden", "grapi", "30", "rent_pct", "cost"))]
    print("candidate burden columns:", burden_cols[:8])
    if not burden_cols:
        sys.exit("no cost-burden column found - paste the ACS column list back to the chat")
    bc = burden_cols[0]
    a["_tract"] = a[aid].astype(str).str[-6:]
    t = t.merge(a[["_tract", bc]].drop_duplicates("_tract"), on="_tract", how="left")
    t[bc] = pd.to_numeric(t[bc], errors="coerce")
    print(f"burden column used: {bc} | tracts with value: {t[bc].notna().sum()}")

    out = {"county_entity_rate_pct": round(county_rate, 3), "burden_col": bc,
           "definitions": {}}
    print(f"\n{'definition':34} {'tracts':>7} {'rate in burdened':>16} {'ratio':>7}")
    for label, mask in [
        ("above county median burden", t[bc] > t[bc].median()),
        ("top quartile burden", t[bc] >= t[bc].quantile(0.75)),
        ("burden >= 30%", t[bc] >= 30),
        ("burden >= 35%", t[bc] >= 35),
        ("burden >= 40%", t[bc] >= 40),
    ]:
        sel = t[mask & t[bc].notna()]
        if not len(sel):
            continue
        # parcel-weighted rate inside burdened tracts
        rate = 100 * sel["entity_n"].sum() / sel["framework_n"].sum()
        ratio = rate / county_rate
        out["definitions"][label] = {"tracts": int(len(sel)),
                                     "rate_pct": round(rate, 3),
                                     "ratio": round(ratio, 3)}
        star = "  <-- 1.47x?" if abs(ratio - 1.47) < 0.06 else ""
        print(f"{label:34} {len(sel):>7} {rate:>15.2f}% {ratio:>6.2f}x{star}")

    json.dump(out, open("burdened_tract_rerun.json", "w"), indent=1)
    print("\nwrote burdened_tract_rerun.json  >>> upload it into the chat")


if __name__ == "__main__":
    for f in (CANON, GEO, ACS):
        if not os.path.exists(f):
            sys.exit(f"missing {f} - run from Key_datasets")
    main()
