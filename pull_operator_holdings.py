#!/usr/bin/env python3
"""
Pull Invitation Homes and American Homes 4 Rent parcel holdings from parcel
GIS endpoints in their major markets.

For each endpoint the script reads the layer metadata, finds the owner name
fields, builds a where clause from known SEC filing entity name patterns,
downloads matching parcels with geometry, and writes one GeoJSON and one CSV
per market per operator plus a summary CSV of counts.

Run with no arguments:
  python3 pull_operator_holdings.py

Optional:
  python3 pull_operator_holdings.py --operator invh          # one operator
  python3 pull_operator_holdings.py --like "TRICON%"         # custom pattern
  python3 pull_operator_holdings.py --market "Wake NC"       # one market

Outputs land in ~/Desktop/Master_Data/SFR_Markets/
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

# Direct parcel layers. A service URL also works. The script picks the first
# layer that exposes an owner style field.
ENDPOINTS = [
    ("Davidson_TN", "https://maps.nashville.gov/arcgis/rest/services/Cadastral/Cadastral_Layers/MapServer/4"),
    ("TN_Statewide_IMPACT", "https://maps.cot.tn.gov/server3/rest/services/IMPACT/Labels_Reappraisal/FeatureServer/13"),
    ("Fulton_GA", "https://gismaps.fultoncountyga.gov/arcgispub2/rest/services/PropertyMapViewer/PropertyMapViewer/MapServer/11"),
    ("Atlanta_City_GA", "https://services5.arcgis.com/5RxyIIJ9boPdptdo/arcgis/rest/services/coa_tax_parcels/FeatureServer/0"),
    ("Maricopa_AZ", "https://gis.mcassessor.maricopa.gov/arcgis/rest/services/MaricopaDynamicQueryService/MapServer/3"),
    ("Collin_TX", "https://services2.arcgis.com/uXyoacYrZTPTKD3R/ArcGIS/rest/services/CCAD_Parcel_Feature_Set/FeatureServer/4"),
    ("Palm_Beach_FL", "https://services1.arcgis.com/RTiKiFNGzgAobBzy/arcgis/rest/services/Parcels/FeatureServer/0"),
    ("FL_Statewide", "https://services9.arcgis.com/Gh9awoU677aKree0/arcgis/rest/services/Florida_Statewide_Cadastral/FeatureServer/0"),
    ("Wake_NC", "https://maps.wakegov.com/arcgis/rest/services/Property/Parcels/MapServer/0"),
    ("NC_Statewide", "https://services.nconemap.gov/secure/rest/services/NC1Map_Parcels/FeatureServer"),
    ("Marion_IN", "https://gis.indy.gov/server/rest/services/MapIndy/MapIndyProperty/MapServer/10"),
    ("MA_Statewide", "https://services1.arcgis.com/hGdibHYSPO59RG1h/arcgis/rest/services/Massachusetts_Property_Tax_Parcels/FeatureServer/0"),
    ("Jefferson_KY", "https://services1.arcgis.com/79kfd2K6fskCAkyg/arcgis/rest/services/LOJIC_Parcels/FeatureServer/0"),
    ("NV_Statewide", "https://gis.dot.nv.gov/agsphs/rest/services/Reference/Statewide_Parcels/MapServer"),
    ("TX_Statewide", "https://feature.geographic.texas.gov/arcgis/rest/services/Parcels/stratmap23_land_parcels_48/MapServer"),
]

# Entity name patterns from SEC filings and securitization documents.
# Matched case insensitive against every owner field the layer exposes.
OPERATORS = {
    "invh": [
        "INVITATION HOMES%",
        "IH2 PROPERTY%", "IH3 PROPERTY%", "IH4 PROPERTY%",
        "IH5 PROPERTY%", "IH6 PROPERTY%",
        "IH PORTFOLIO%",
        "THR PROPERTY%",          # original Blackstone entities
        "CSH PROPERTY%",          # Colony Starwood
        "COLONY AMERICAN HOMES%",
        "STARWOOD WAYPOINT%",
        "SRP SUB%",               # Starwood Waypoint borrower
    ],
    "amh": [
        "AMERICAN HOMES 4 RENT%",
        "AMH 201%", "AMH 202%",   # AMH 2014-SFR1 style borrowers
        "AMH DEVELOPMENT%",
        "AMH PORTFOLIO%",
        "AH4R%",
    ],
}

OWNER_HINTS = ("OWNER", "OWN_NAME", "OWNNAME", "OWNERNAME", "OWNER_NAME",
               "OWNJAN1", "OWN1", "PROPRIETOR", "TAXPAYER", "DEEDHOLDER")


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
    """Return (layer_url, metadata) for a layer with an owner field.
    Accepts a layer url or a service url."""
    meta = get_json(url)
    if "fields" in meta:
        return url, meta
    for lyr in meta.get("layers", []) or []:
        lurl = f"{url.rstrip('/')}/{lyr['id']}"
        try:
            lmeta = get_json(lurl)
        except Exception:  # noqa: BLE001
            continue
        if owner_fields(lmeta):
            return lurl, lmeta
    return None, meta


def owner_fields(meta):
    out = []
    for f in meta.get("fields", []) or []:
        name = f["name"]
        if any(h in name.upper() for h in OWNER_HINTS) and \
                f.get("type") == "esriFieldTypeString":
            out.append(name)
    # Owner fields only. Drop mailing-city style false hits.
    return [n for n in out if "CITY" not in n.upper() and "ADDR" not in n.upper()][:4]


def build_where(fields, patterns):
    clauses = []
    for f in fields:
        for p in patterns:
            clauses.append(f"UPPER({f}) LIKE '{p.upper()}'")
    return " OR ".join(clauses)


def esri_to_geojson_feature(f, gtype):
    geom = f.get("geometry")
    gj = None
    if geom:
        if gtype == "esriGeometryPoint":
            gj = {"type": "Point", "coordinates": [geom.get("x"), geom.get("y")]}
        elif gtype == "esriGeometryPolygon":
            gj = {"type": "Polygon", "coordinates": geom.get("rings", [])}
        elif gtype == "esriGeometryPolyline":
            paths = geom.get("paths", [])
            gj = {"type": "MultiLineString", "coordinates": paths}
    return {"type": "Feature", "geometry": gj,
            "properties": f.get("attributes", {})}


def query_all(layer_url, meta, where):
    gtype = meta.get("geometryType")
    oid = meta.get("objectIdField") or next(
        (f["name"] for f in meta.get("fields", [])
         if f["type"] == "esriFieldTypeOID"), "OBJECTID")
    batch = min(int(meta.get("maxRecordCount") or 1000), 2000)
    feats = []
    offset = 0
    while True:
        params = {"where": where, "outFields": "*", "outSR": 4326,
                  "returnGeometry": "true", "orderByFields": oid,
                  "resultOffset": offset, "resultRecordCount": batch}
        try:
            data = get_json(f"{layer_url}/query", {**params, "f": "geojson"})
            page = data.get("features", [])
        except Exception:  # noqa: BLE001
            data = get_json(f"{layer_url}/query", {**params, "f": "json"})
            page = [esri_to_geojson_feature(f, gtype)
                    for f in data.get("features", [])]
        feats.extend(page)
        if len(page) < batch:
            break
        offset += len(page)
        print(f"      ...{len(feats)} so far")
    return feats


def save(feats, outdir, name):
    os.makedirs(outdir, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")
    stem = os.path.join(outdir, f"{name}_{date_str}")
    with open(stem + ".geojson", "w") as f:
        json.dump({"type": "FeatureCollection", "features": feats}, f)
    cols = []
    for ft in feats:
        for k in ft.get("properties", {}):
            if k not in cols:
                cols.append(k)
    with open(stem + ".csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for ft in feats:
            w.writerow(ft.get("properties", {}))
    return stem


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--operator", choices=list(OPERATORS), default=None,
                    help="only this operator (default: all)")
    ap.add_argument("--like", default=None,
                    help="custom owner pattern, e.g. \"TRICON%%\"")
    ap.add_argument("--market", default=None,
                    help="only markets whose name contains this text")
    ap.add_argument("--outdir",
                    default=os.path.expanduser("~/Desktop/Master_Data/SFR_Markets"))
    args = ap.parse_args()

    if args.like:
        operators = {"custom": [args.like]}
    elif args.operator:
        operators = {args.operator: OPERATORS[args.operator]}
    else:
        operators = OPERATORS

    endpoints = [(m, u) for m, u in ENDPOINTS
                 if not args.market or args.market.lower() in m.lower()]

    summary = []
    for market, url in endpoints:
        print(f"\n=== {market} ===")
        try:
            layer_url, meta = resolve_layer(url)
        except Exception as e:  # noqa: BLE001
            print(f"  UNREACHABLE: {e}")
            summary.append([market, "-", "UNREACHABLE", ""])
            continue
        if not layer_url:
            print("  no layer with an owner field found, skipping")
            summary.append([market, "-", "no owner field", ""])
            continue
        fields = owner_fields(meta)
        print(f"  layer: {meta.get('name')} | owner fields: {fields}")
        for op, patterns in operators.items():
            where = build_where(fields, patterns)
            try:
                feats = query_all(layer_url, meta, where)
            except Exception as e:  # noqa: BLE001
                print(f"    {op}: query failed: {e}")
                summary.append([market, op, "query failed", str(e)[:80]])
                continue
            if feats:
                stem = save(feats, args.outdir, f"{market}_{op}")
                print(f"    {op}: {len(feats)} parcels -> {stem}.csv")
                summary.append([market, op, len(feats), stem + ".csv"])
            else:
                print(f"    {op}: 0 parcels")
                summary.append([market, op, 0, ""])

    date_str = datetime.now().strftime("%Y%m%d")
    os.makedirs(args.outdir, exist_ok=True)
    sum_path = os.path.join(args.outdir, f"operator_holdings_summary_{date_str}.csv")
    with open(sum_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["market", "operator", "parcels", "file"])
        w.writerows(summary)
    print(f"\nSummary saved: {sum_path}")
    print("\nMarket        Operator  Parcels")
    for row in summary:
        print(f"{row[0]:<22} {row[1]:<8} {row[2]}")


if __name__ == "__main__":
    main()
