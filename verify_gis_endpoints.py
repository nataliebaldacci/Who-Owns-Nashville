#!/usr/bin/env python3
"""
Probe candidate parcel GIS endpoints for major corporate landlord markets.

For each endpoint this script reports whether it is reachable, what parcel
layers it exposes, how many features each holds, and which field looks like
the owner name. It writes a CSV inventory you can use to build pull commands
for pull_tennessee_gis.py.

Run:
  python3 verify_gis_endpoints.py

Output:
  ~/Desktop/Master_Data/SFR_Markets/gis_endpoint_inventory_[date].csv
"""

import csv
import json
import os
from datetime import datetime

import requests

TIMEOUT = 30

# (market, kind, url) where kind is "layer", "service", or "root".
ENDPOINTS = [
    ("TN statewide boundaries", "layer",
     "https://services1.arcgis.com/YuVBSS7Y1of2Qud1/arcgis/rest/services/Tennessee_Property_Boundaries_Public_Use/FeatureServer/0"),
    ("TN statewide assessment (IMPACT)", "layer",
     "https://maps.cot.tn.gov/server3/rest/services/IMPACT/Labels_Reappraisal/FeatureServer/13"),
    ("FL statewide (Tampa/Jax/Orlando)", "layer",
     "https://services9.arcgis.com/Gh9awoU677aKree0/arcgis/rest/services/Florida_Statewide_Cadastral/FeatureServer/0"),
    ("NC statewide (Charlotte/Raleigh)", "service",
     "https://services.nconemap.gov/secure/rest/services/NC1Map_Parcels/FeatureServer"),
    ("Charlotte county fallback", "service",
     "https://gis.charlottenc.gov/arcgis/rest/services/CountyData/Parcels/MapServer"),
    ("TX statewide (DFW/Houston)", "service",
     "https://feature.geographic.texas.gov/arcgis/rest/services/Parcels/stratmap23_land_parcels_48/MapServer"),
    ("Memphis - Shelby Co TN assessor", "service",
     "https://gis.shelbycountytn.gov/public/rest/services/BaseMap/Assessor/MapServer"),
    ("Memphis - Shelby Co TN root", "root",
     "https://gis.shelbycountytn.gov/arcgis/rest/services"),
    ("Knoxville - Knox Co TN root", "root",
     "https://www.kgis.org/arcgis/rest/services"),
    ("Atlanta - Fulton Co GA root", "root",
     "https://gismaps.fultoncountyga.gov/arcgispub2/rest/services"),
    ("Atlanta - DeKalb Co GA root", "root",
     "https://dcgis.dekalbcountyga.gov/hosted/rest/services"),
    ("Atlanta - regional commission root", "root",
     "https://arcgis.atlantaregional.com/arcgis/rest/services"),
    ("Phoenix - Maricopa Co AZ parcels", "layer",
     "https://gis.mcassessor.maricopa.gov/arcgis/rest/services/MaricopaDynamicQueryService/MapServer/3"),
    ("Las Vegas - Clark Co NV root", "root",
     "https://maps.clarkcountynv.gov/arcgis/rest/services"),
    ("Las Vegas - Clark Co NV root 2", "root",
     "https://gisgate.co.clark.nv.us/arcgis/rest/services"),
    ("Nevada statewide fallback", "service",
     "https://arcgis.water.nv.gov/arcgis/rest/services/BaseLayers/County_Parcels_in_Nevada/MapServer"),
    ("Indianapolis - Marion Co IN root", "root",
     "https://xmaps.indy.gov/arcgis/rest/services"),
]

OWNER_HINTS = ("OWNER", "OWN_NAME", "OWNNAME", "OWNERNAME", "OWNER_NAME",
               "OWN_NAME1", "OWNNAME1", "OWNJAN1", "DEEDHOLDER", "PROPRIETOR")
PARCEL_HINTS = ("PARCEL", "CADASTRAL", "TAX", "PROPERTY", "ASSESS", "LAND")


def get_json(url, params=None):
    params = dict(params or {})
    params.setdefault("f", "json")
    r = requests.get(url, params=params, timeout=TIMEOUT)
    r.raise_for_status()
    data = r.json()
    if isinstance(data, dict) and "error" in data:
        raise RuntimeError(str(data["error"])[:120])
    return data


def owner_fields(meta):
    names = [f["name"] for f in meta.get("fields", []) or []]
    return [n for n in names if any(h in n.upper() for h in OWNER_HINTS)]


def feature_count(layer_url):
    try:
        return get_json(f"{layer_url}/query",
                        {"where": "1=1", "returnCountOnly": "true"}).get("count")
    except Exception:  # noqa: BLE001
        return None


def check_layer(market, layer_url, rows, note=""):
    try:
        meta = get_json(layer_url)
    except Exception as e:  # noqa: BLE001
        rows.append([market, layer_url, "ERROR", "", "", "", str(e)[:100]])
        print(f"  ERROR {layer_url}: {e}")
        return
    if "fields" not in meta:
        rows.append([market, layer_url, "no-fields", "", "", "", note])
        return
    own = owner_fields(meta)
    cnt = feature_count(layer_url)
    status = "OK owner-data" if own and cnt else ("OK" if cnt else "empty/blocked")
    rows.append([market, layer_url, status, meta.get("name", ""),
                 cnt if cnt is not None else "", ";".join(own), note])
    print(f"  {status}: {meta.get('name','?')} count={cnt} owner_fields={own}")


def check_service(market, svc_url, rows):
    try:
        meta = get_json(svc_url)
    except Exception as e:  # noqa: BLE001
        rows.append([market, svc_url, "ERROR", "", "", "", str(e)[:100]])
        print(f"  ERROR {svc_url}: {e}")
        return
    layers = meta.get("layers", []) or []
    if not layers:
        rows.append([market, svc_url, "no-layers", "", "", "", ""])
        return
    for lyr in layers:
        looks_parcel = any(h in lyr["name"].upper() for h in PARCEL_HINTS)
        if looks_parcel or len(layers) <= 8:
            check_layer(market, f"{svc_url}/{lyr['id']}", rows)


def check_root(market, root_url, rows):
    try:
        meta = get_json(root_url)
    except Exception as e:  # noqa: BLE001
        rows.append([market, root_url, "ERROR", "", "", "", str(e)[:100]])
        print(f"  ERROR {root_url}: {e}")
        return
    base = root_url.split("/rest/services")[0] + "/rest/services"
    svcs = meta.get("services", []) or []
    folders = meta.get("folders", []) or []
    # One level of folders is enough for discovery.
    for folder in folders:
        try:
            sub = get_json(f"{base}/{folder}")
            svcs.extend(sub.get("services", []) or [])
        except Exception:  # noqa: BLE001
            continue
    hits = [s for s in svcs
            if any(h in s["name"].upper() for h in PARCEL_HINTS)
            and s["type"] in ("MapServer", "FeatureServer")]
    print(f"  root has {len(svcs)} services, {len(hits)} look parcel-related")
    rows.append([market, root_url, "root", "", len(svcs), "",
                 "parcel-like: " + "; ".join(s["name"] for s in hits[:12])])
    for s in hits[:6]:
        check_service(market, f"{base}/{s['name']}/{s['type']}", rows)


def main():
    outdir = os.path.expanduser("~/Desktop/Master_Data/SFR_Markets")
    os.makedirs(outdir, exist_ok=True)
    rows = []
    for market, kind, url in ENDPOINTS:
        print(f"\n=== {market} ===\n  {url}")
        try:
            if kind == "layer":
                check_layer(market, url, rows)
            elif kind == "service":
                check_service(market, url, rows)
            else:
                check_root(market, url, rows)
        except Exception as e:  # noqa: BLE001
            rows.append([market, url, "ERROR", "", "", "", str(e)[:100]])
            print(f"  ERROR: {e}")

    date_str = datetime.now().strftime("%Y%m%d")
    out_path = os.path.join(outdir, f"gis_endpoint_inventory_{date_str}.csv")
    with open(out_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["market", "url", "status", "layer_name",
                    "feature_count", "owner_fields", "notes"])
        w.writerows(rows)
    print(f"\nSaved inventory: {out_path}")
    print("Rows with status 'OK owner-data' are ready for pull_tennessee_gis.py")


if __name__ == "__main__":
    main()
