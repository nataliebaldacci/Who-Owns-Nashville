#!/usr/bin/env python3
"""
Pull absentee owned parcels from parcel GIS endpoints in major markets.

Absentee means the owner mailing zip does not match the property zip. When a
layer lacks one of the two zip fields the script falls back to out of state
mailing address. Add --corporate to also require a business style owner name
(LLC, LP, Inc, Trust, Holdings, Properties and similar).

Always run a survey first to see counts before downloading anything:

  python3 pull_absentee_owners.py --count-only

Then pull one market:

  python3 pull_absentee_owners.py --market FL_Statewide

Or everything:

  python3 pull_absentee_owners.py

Outputs (attributes only, no geometry, so files stay small) land in
~/Desktop/Master_Data/SFR_Markets/ as CSV plus raw NDJSON.
"""

import argparse
import csv
import json
import os
import time
from datetime import datetime

import requests

TIMEOUT = 60
MAX_RETRIES = 4

# (market, home_state, layer or service url)
ENDPOINTS = [
    ("Davidson_TN", "TN", "https://maps.nashville.gov/arcgis/rest/services/Cadastral/Cadastral_Layers/MapServer/4"),
    ("TN_Statewide_IMPACT", "TN", "https://maps.cot.tn.gov/server3/rest/services/IMPACT/Labels_Reappraisal/FeatureServer/13"),
    ("Fulton_GA", "GA", "https://gismaps.fultoncountyga.gov/arcgispub2/rest/services/PropertyMapViewer/PropertyMapViewer/MapServer/11"),
    ("Atlanta_City_GA", "GA", "https://services5.arcgis.com/5RxyIIJ9boPdptdo/arcgis/rest/services/coa_tax_parcels/FeatureServer/0"),
    ("Maricopa_AZ", "AZ", "https://gis.mcassessor.maricopa.gov/arcgis/rest/services/MaricopaDynamicQueryService/MapServer/3"),
    ("Collin_TX", "TX", "https://services2.arcgis.com/uXyoacYrZTPTKD3R/ArcGIS/rest/services/CCAD_Parcel_Feature_Set/FeatureServer/4"),
    ("Palm_Beach_FL", "FL", "https://services1.arcgis.com/RTiKiFNGzgAobBzy/arcgis/rest/services/Parcels/FeatureServer/0"),
    ("FL_Statewide", "FL", "https://services9.arcgis.com/Gh9awoU677aKree0/arcgis/rest/services/Florida_Statewide_Cadastral/FeatureServer/0"),
    ("Wake_NC", "NC", "https://maps.wakegov.com/arcgis/rest/services/Property/Parcels/MapServer/0"),
    ("NC_Statewide", "NC", "https://services.nconemap.gov/secure/rest/services/NC1Map_Parcels/FeatureServer"),
    ("Marion_IN", "IN", "https://gis.indy.gov/server/rest/services/MapIndy/MapIndyProperty/MapServer/10"),
    ("MA_Statewide", "MA", "https://services1.arcgis.com/hGdibHYSPO59RG1h/arcgis/rest/services/Massachusetts_Property_Tax_Parcels/FeatureServer/0"),
    ("Jefferson_KY", "KY", "https://services1.arcgis.com/79kfd2K6fskCAkyg/arcgis/rest/services/LOJIC_Parcels/FeatureServer/0"),
    ("NV_Statewide", "NV", "https://gis.dot.nv.gov/agsphs/rest/services/Reference/Statewide_Parcels/MapServer"),
    ("TX_Statewide", "TX", "https://feature.geographic.texas.gov/arcgis/rest/services/Parcels/stratmap23_land_parcels_48/MapServer"),
]

OWNER_ZIP_HINTS = ("OWN_ZIP", "OWNZIP", "MAIL_ZIP", "MAILZIP", "MZIP",
                   "OWNER_ZIP", "TAXPAYER_ZIP")
PROP_ZIP_HINTS = ("PHY_ZIP", "PROP_ZIP", "PROPZIP", "SITE_ZIP", "SITUS_ZIP",
                  "SITEZIP", "SITUSZIP", "LOC_ZIP", "PZIP", "PARCEL_ZIP")
OWNER_STATE_HINTS = ("OWN_STATE", "OWNSTATE", "MAIL_STATE", "MAILSTATE",
                     "OWNER_STATE", "MSTATE", "OWN_ST", "MAIL_ST")
OWNER_NAME_HINTS = ("OWNER", "OWN_NAME", "OWNNAME", "OWNERNAME", "OWNER_NAME",
                    "OWNJAN1", "TAXPAYER")

CORPORATE_PATTERNS = ("% LLC%", "%L L C%", "% LP", "% L P", "%LTD%", "% INC%",
                      "%CORP%", "%TRUST%", "%HOLDINGS%", "%PROPERTIES%",
                      "%PARTNERS%", "%INVEST%", "%HOMES%", "%RENTAL%",
                      "%CAPITAL%", "%VENTURES%", "%FUND%", "%REALTY%")


def get_json(url, params=None):
    params = dict(params or {})
    params.setdefault("f", "json")
    last = None
    for attempt in range(MAX_RETRIES):
        try:
            r = requests.get(url, params=params, timeout=TIMEOUT)
            r.raise_for_status()
            data = r.json()
            if isinstance(data, dict) and "error" in data:
                raise RuntimeError(str(data["error"])[:150])
            return data
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2 ** attempt)
    raise RuntimeError(f"{url}: {last}")


def resolve_layer(url):
    meta = get_json(url)
    if "fields" in meta:
        return url, meta
    for lyr in meta.get("layers", []) or []:
        lurl = f"{url.rstrip('/')}/{lyr['id']}"
        try:
            lmeta = get_json(lurl)
        except Exception:  # noqa: BLE001
            continue
        if find_field(lmeta, OWNER_NAME_HINTS):
            return lurl, lmeta
    return None, meta


def find_field(meta, hints):
    names = [f["name"] for f in meta.get("fields", []) or []
             if f.get("type") == "esriFieldTypeString"]
    for hint in hints:
        for n in names:
            if hint in n.upper():
                return n
    return None


def build_filter(meta, home_state, corporate):
    """Return (where, mode). Prefers zip mismatch, falls back to state."""
    ozip = find_field(meta, OWNER_ZIP_HINTS)
    pzip = find_field(meta, PROP_ZIP_HINTS)
    ostate = find_field(meta, OWNER_STATE_HINTS) or find_field(meta, ("STATE",))
    parts = []
    mode = None
    if ozip and pzip and ozip != pzip:
        parts.append(f"{ozip} <> {pzip} AND {ozip} IS NOT NULL AND {pzip} IS NOT NULL")
        mode = f"zip mismatch ({ozip} vs {pzip})"
    elif ostate:
        parts.append(f"UPPER({ostate}) <> '{home_state}' AND {ostate} IS NOT NULL AND {ostate} <> ''")
        mode = f"out of state ({ostate})"
    else:
        return None, "no owner zip or state field"
    if corporate:
        oname = find_field(meta, OWNER_NAME_HINTS)
        if oname:
            likes = " OR ".join(f"UPPER({oname}) LIKE '{p}'" for p in CORPORATE_PATTERNS)
            parts.append(f"({likes})")
            mode += " + corporate name"
    return " AND ".join(f"({p})" for p in parts), mode


def count(layer_url, where):
    return get_json(f"{layer_url}/query",
                    {"where": where, "returnCountOnly": "true"}).get("count")


def pull(layer_url, meta, where, outdir, name, ozip_pair):
    oid = meta.get("objectIdField") or next(
        (f["name"] for f in meta.get("fields", [])
         if f["type"] == "esriFieldTypeOID"), "OBJECTID")
    batch = min(int(meta.get("maxRecordCount") or 1000), 2000)
    os.makedirs(outdir, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")
    stem = os.path.join(outdir, f"{name}_{date_str}")
    nd_path = stem + ".ndjson"

    done = 0
    if os.path.exists(nd_path):
        with open(nd_path) as f:
            done = sum(1 for _ in f)
        print(f"    resuming at {done}")

    total = count(layer_url, where)
    offset = done
    with open(nd_path, "a") as out:
        while offset < total:
            data = get_json(f"{layer_url}/query", {
                "where": where, "outFields": "*", "returnGeometry": "false",
                "orderByFields": oid, "resultOffset": offset,
                "resultRecordCount": batch})
            feats = data.get("features", [])
            if not feats:
                break
            for f in feats:
                out.write(json.dumps(f.get("attributes", {})) + "\n")
            out.flush()
            offset += len(feats)
            print(f"    {offset}/{total}")

    # CSV, with a zip5 recheck to drop zip9 vs zip5 false mismatches.
    kept = 0
    with open(nd_path) as src, open(stem + ".csv", "w", newline="") as f:
        writer = None
        for line in src:
            row = json.loads(line)
            if ozip_pair:
                oz = str(row.get(ozip_pair[0]) or "")[:5]
                pz = str(row.get(ozip_pair[1]) or "")[:5]
                if oz and pz and oz == pz:
                    continue
            if writer is None:
                writer = csv.DictWriter(f, fieldnames=list(row.keys()),
                                        extrasaction="ignore")
                writer.writeheader()
            writer.writerow(row)
            kept += 1
    print(f"    saved {kept} rows -> {stem}.csv")
    return kept


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--count-only", action="store_true",
                    help="survey counts, download nothing")
    ap.add_argument("--corporate", action="store_true",
                    help="also require business style owner name")
    ap.add_argument("--market", default=None,
                    help="only markets whose name contains this text")
    ap.add_argument("--outdir",
                    default=os.path.expanduser("~/Desktop/Master_Data/SFR_Markets"))
    args = ap.parse_args()

    endpoints = [(m, s, u) for m, s, u in ENDPOINTS
                 if not args.market or args.market.lower() in m.lower()]

    summary = []
    for market, home_state, url in endpoints:
        print(f"\n=== {market} ===")
        try:
            layer_url, meta = resolve_layer(url)
        except Exception as e:  # noqa: BLE001
            print(f"  UNREACHABLE: {e}")
            summary.append([market, "UNREACHABLE", "", ""])
            continue
        if not layer_url:
            print("  no usable layer found")
            summary.append([market, "no layer", "", ""])
            continue
        where, mode = build_filter(meta, home_state, args.corporate)
        if not where:
            print(f"  skipped: {mode}")
            summary.append([market, mode, "", ""])
            continue
        try:
            n = count(layer_url, where)
        except Exception as e:  # noqa: BLE001
            print(f"  count failed: {e}")
            summary.append([market, f"count failed: {str(e)[:60]}", "", ""])
            continue
        print(f"  {mode}: {n} parcels")
        if args.count_only:
            summary.append([market, mode, n, "not downloaded"])
            continue
        ozip = find_field(meta, OWNER_ZIP_HINTS)
        pzip = find_field(meta, PROP_ZIP_HINTS)
        pair = (ozip, pzip) if (ozip and pzip and "zip" in mode) else None
        suffix = "absentee_corp" if args.corporate else "absentee"
        try:
            kept = pull(layer_url, meta, where, args.outdir,
                        f"{market}_{suffix}", pair)
            summary.append([market, mode, kept, "downloaded"])
        except Exception as e:  # noqa: BLE001
            print(f"  pull failed: {e}")
            summary.append([market, mode, n, f"pull failed: {str(e)[:60]}"])

    print("\nMarket                 Filter                          Parcels")
    for row in summary:
        print(f"{row[0]:<22} {str(row[1]):<32} {row[2]}")

    os.makedirs(args.outdir, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")
    with open(os.path.join(args.outdir, f"absentee_survey_{date_str}.csv"),
              "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["market", "filter_mode", "parcels", "status"])
        w.writerows(summary)


if __name__ == "__main__":
    main()
