#!/usr/bin/env python3
"""
Pull data from Tennessee statewide ArcGIS REST services.

Targets:
  1. Comptroller IMPACT folder (ArcGIS Server):
     https://maps.cot.tn.gov/server3/rest/services/IMPACT
     - includes IMPACT/Parcel_Layer_Themes/FeatureServer (assessment-themed
       statewide parcel layers)
  2. Statewide parcel boundaries (ArcGIS Online hosted):
     https://services1.arcgis.com/YuVBSS7Y1of2Qud1/arcgis/rest/services/Tennessee_Property_Boundaries_Public_Use/FeatureServer/0

Usage examples:

  # See what exists: folders, services, layers, fields, feature counts
  python3 pull_tennessee_gis.py inspect "https://maps.cot.tn.gov/server3/rest/services/IMPACT"
  python3 pull_tennessee_gis.py inspect "https://services1.arcgis.com/YuVBSS7Y1of2Qud1/arcgis/rest/services/Tennessee_Property_Boundaries_Public_Use/FeatureServer/0"

  # Pull one layer completely (paginated, resumable)
  python3 pull_tennessee_gis.py pull \
      "https://services1.arcgis.com/YuVBSS7Y1of2Qud1/arcgis/rest/services/Tennessee_Property_Boundaries_Public_Use/FeatureServer/0" \
      --name TN_Parcels_Davidson --where "COUNTY = 'DAVIDSON'"

  # Pull attributes only (no geometry) for the whole state
  python3 pull_tennessee_gis.py pull \
      "https://services1.arcgis.com/YuVBSS7Y1of2Qud1/arcgis/rest/services/Tennessee_Property_Boundaries_Public_Use/FeatureServer/0" \
      --name TN_Parcels_Statewide_attrs --no-geometry

  # Pull every layer of every service in a folder
  python3 pull_tennessee_gis.py pull-folder "https://maps.cot.tn.gov/server3/rest/services/IMPACT" \
      --outdir ~/Desktop/Master_Data/TN_Statewide

Outputs both GeoJSON and CSV for each layer. Downloads stream to a newline
delimited .ndjson file first so an interrupted pull resumes where it left off.
Run the exact same command again to resume.

Field names differ by service. Run inspect first, then build your --where
clause from the real field names it prints.
"""

import argparse
import csv
import json
import os
import sys
import time
from datetime import datetime

import requests

BATCH_FALLBACK = 1000
TIMEOUT = 120
MAX_RETRIES = 5


def get_json(url, params=None):
    """GET with retries and exponential backoff. Raises on persistent failure."""
    params = dict(params or {})
    params.setdefault("f", "json")
    last_err = None
    for attempt in range(MAX_RETRIES):
        try:
            r = requests.get(url, params=params, timeout=TIMEOUT)
            r.raise_for_status()
            data = r.json()
            if isinstance(data, dict) and "error" in data:
                raise RuntimeError(f"ArcGIS error: {data['error']}")
            return data
        except Exception as e:  # noqa: BLE001
            last_err = e
            wait = 2 ** (attempt + 1)
            print(f"  retry {attempt + 1}/{MAX_RETRIES} after error: {e} (waiting {wait}s)")
            time.sleep(wait)
    raise RuntimeError(f"Failed after {MAX_RETRIES} retries: {url} :: {last_err}")


# ---------------------------------------------------------------- inspect ---

def inspect_url(url):
    """Print what lives at an ArcGIS REST url: folder, service, or layer."""
    url = url.rstrip("/")
    data = get_json(url)

    if "fields" in data and "geometryType" in data or "fields" in data and data.get("type") == "Table":
        inspect_layer(url, data)
        return

    if "layers" in data or "tables" in data:
        print(f"SERVICE: {url}")
        for lyr in data.get("layers", []):
            print(f"  layer {lyr['id']}: {lyr['name']}")
            inspect_layer(f"{url}/{lyr['id']}")
        for tbl in data.get("tables", []):
            print(f"  table {tbl['id']}: {tbl['name']}")
            inspect_layer(f"{url}/{tbl['id']}")
        return

    if "services" in data or "folders" in data:
        print(f"FOLDER: {url}")
        for folder in data.get("folders", []):
            print(f"  subfolder: {folder}")
        root = url.split("/rest/services")[0] + "/rest/services"
        for svc in data.get("services", []):
            svc_url = f"{root}/{svc['name']}/{svc['type']}"
            print(f"\n  service: {svc['name']} ({svc['type']})")
            if svc["type"] in ("FeatureServer", "MapServer"):
                try:
                    inspect_url(svc_url)
                except Exception as e:  # noqa: BLE001
                    print(f"    could not read service: {e}")
        return

    print(json.dumps(data, indent=2)[:3000])


def inspect_layer(layer_url, meta=None):
    meta = meta or get_json(layer_url)
    name = meta.get("name", "?")
    gtype = meta.get("geometryType", "table")
    maxrec = meta.get("maxRecordCount", "?")
    adv = meta.get("advancedQueryCapabilities", {}) or {}
    pag = adv.get("supportsPagination", meta.get("supportsPagination", False))
    try:
        cnt = get_json(f"{layer_url}/query", {"where": "1=1", "returnCountOnly": "true"}).get("count", "?")
    except Exception:  # noqa: BLE001
        cnt = "?"
    print(f"    {layer_url}")
    print(f"    name={name} geom={gtype} count={cnt} maxRecordCount={maxrec} pagination={pag}")
    for f in meta.get("fields", []) or []:
        print(f"      {f['name']} ({f['type']})")


# ------------------------------------------------------------------- pull ---

def esri_geom_to_geojson(geom, gtype):
    """Convert esriJSON geometry to GeoJSON. Used when f=geojson is unsupported."""
    if geom is None:
        return None
    if gtype == "esriGeometryPoint":
        return {"type": "Point", "coordinates": [geom.get("x"), geom.get("y")]}
    if gtype == "esriGeometryMultipoint":
        return {"type": "MultiPoint", "coordinates": geom.get("points", [])}
    if gtype == "esriGeometryPolyline":
        paths = geom.get("paths", [])
        if len(paths) == 1:
            return {"type": "LineString", "coordinates": paths[0]}
        return {"type": "MultiLineString", "coordinates": paths}
    if gtype in ("esriGeometryPolygon", "esriGeometryEnvelope"):
        rings = geom.get("rings", [])
        return {"type": "Polygon", "coordinates": rings}
    return None


def fetch_batch(layer_url, params, geojson_ok, gtype):
    """Fetch one page of features. Returns (features, exceeded, geojson_ok)."""
    if geojson_ok:
        try:
            data = get_json(f"{layer_url}/query", {**params, "f": "geojson"})
            feats = data.get("features", [])
            exceeded = bool(data.get("exceededTransferLimit")) or bool(
                (data.get("properties") or {}).get("exceededTransferLimit"))
            return feats, exceeded, True
        except Exception as e:  # noqa: BLE001
            print(f"  f=geojson failed ({e}); falling back to esriJSON")
    data = get_json(f"{layer_url}/query", {**params, "f": "json"})
    feats = []
    for f in data.get("features", []):
        feats.append({
            "type": "Feature",
            "geometry": esri_geom_to_geojson(f.get("geometry"), gtype),
            "properties": f.get("attributes", {}),
        })
    return feats, bool(data.get("exceededTransferLimit")), False


def pull_layer(layer_url, name, where, out_fields, outdir, no_geometry=False):
    layer_url = layer_url.rstrip("/")
    os.makedirs(outdir, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")
    stem = os.path.join(outdir, f"{name}_{date_str}")
    ndjson_path = stem + ".ndjson"

    meta = get_json(layer_url)
    gtype = meta.get("geometryType")
    oid_field = meta.get("objectIdField") or next(
        (f["name"] for f in meta.get("fields", []) if f["type"] == "esriFieldTypeOID"), "OBJECTID")
    maxrec = int(meta.get("maxRecordCount") or BATCH_FALLBACK)
    batch = min(maxrec, 2000)
    adv = meta.get("advancedQueryCapabilities", {}) or {}
    supports_pagination = adv.get("supportsPagination", meta.get("supportsPagination", False))

    total = get_json(f"{layer_url}/query", {"where": where, "returnCountOnly": "true"}).get("count")
    print(f"Layer: {meta.get('name')} | where: {where} | total features: {total}")
    print(f"objectIdField={oid_field} batch={batch} pagination={supports_pagination}")

    # Resume: count features already saved.
    done = 0
    if os.path.exists(ndjson_path):
        with open(ndjson_path) as fh:
            done = sum(1 for _ in fh)
        print(f"Resuming: {done} features already downloaded")

    base_params = {
        "where": where,
        "outFields": out_fields,
        "outSR": 4326,
        "returnGeometry": "false" if no_geometry else "true",
        "orderByFields": oid_field,
    }
    geojson_ok = not no_geometry

    with open(ndjson_path, "a") as out:
        if supports_pagination:
            offset = done
            while offset < (total or 0) or total is None:
                params = {**base_params, "resultOffset": offset, "resultRecordCount": batch}
                feats, exceeded, geojson_ok = fetch_batch(layer_url, params, geojson_ok, gtype)
                for f in feats:
                    out.write(json.dumps(f) + "\n")
                out.flush()
                offset += len(feats)
                print(f"  {offset}/{total} features")
                if not feats or (len(feats) < batch and not exceeded):
                    break
        else:
            # Old servers without pagination: walk OBJECTID ranges.
            ids = get_json(f"{layer_url}/query",
                           {"where": where, "returnIdsOnly": "true"}).get("objectIds") or []
            ids.sort()
            ids = ids[done:]
            print(f"  {len(ids)} ids remaining (of {total})")
            for i in range(0, len(ids), batch):
                chunk = ids[i:i + batch]
                params = {**base_params,
                          "where": f"{oid_field} >= {chunk[0]} AND {oid_field} <= {chunk[-1]} "
                                   f"AND ({where})"}
                feats, _, geojson_ok = fetch_batch(layer_url, params, geojson_ok, gtype)
                for f in feats:
                    out.write(json.dumps(f) + "\n")
                out.flush()
                print(f"  {done + i + len(chunk)}/{total} features")

    write_outputs(ndjson_path, stem, meta, no_geometry)


def write_outputs(ndjson_path, stem, meta, no_geometry):
    """Assemble final GeoJSON and CSV from the ndjson stream without loading
    everything into memory."""
    field_names = [f["name"] for f in meta.get("fields", []) or []]

    csv_path = stem + ".csv"
    geojson_path = stem + ".geojson"

    with open(ndjson_path) as src, open(csv_path, "w", newline="") as csvf:
        writer = None
        n = 0
        for line in src:
            feat = json.loads(line)
            props = feat.get("properties", {})
            if writer is None:
                cols = field_names or list(props.keys())
                extra = [k for k in props.keys() if k not in cols]
                cols = cols + extra
                writer = csv.DictWriter(csvf, fieldnames=cols, extrasaction="ignore")
                writer.writeheader()
            writer.writerow(props)
            n += 1
    print(f"Saved CSV: {csv_path} ({n} rows)")

    if not no_geometry:
        with open(ndjson_path) as src, open(geojson_path, "w") as gj:
            gj.write('{"type":"FeatureCollection","features":[\n')
            first = True
            for line in src:
                if not first:
                    gj.write(",\n")
                gj.write(line.rstrip("\n"))
                first = False
            gj.write("\n]}\n")
        print(f"Saved GeoJSON: {geojson_path}")


def pull_folder(folder_url, outdir, where, out_fields, no_geometry):
    folder_url = folder_url.rstrip("/")
    data = get_json(folder_url)
    root = folder_url.split("/rest/services")[0] + "/rest/services"
    for svc in data.get("services", []):
        if svc["type"] not in ("FeatureServer", "MapServer"):
            print(f"skipping {svc['name']} ({svc['type']})")
            continue
        svc_url = f"{root}/{svc['name']}/{svc['type']}"
        try:
            svc_meta = get_json(svc_url)
        except Exception as e:  # noqa: BLE001
            print(f"could not read {svc_url}: {e}")
            continue
        svc_slug = svc["name"].replace("/", "_")
        for lyr in svc_meta.get("layers", []) + svc_meta.get("tables", []):
            name = f"{svc_slug}_L{lyr['id']}_{lyr['name'].replace(' ', '_')}"
            print(f"\n=== {name} ===")
            try:
                pull_layer(f"{svc_url}/{lyr['id']}", name, where, out_fields, outdir, no_geometry)
            except Exception as e:  # noqa: BLE001
                print(f"FAILED {name}: {e}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_inspect = sub.add_parser("inspect", help="print folders/services/layers/fields/counts")
    p_inspect.add_argument("url")

    p_pull = sub.add_parser("pull", help="download one layer")
    p_pull.add_argument("url")
    p_pull.add_argument("--name", required=True, help="output file stem")
    p_pull.add_argument("--where", default="1=1")
    p_pull.add_argument("--fields", default="*")
    p_pull.add_argument("--outdir", default=os.path.expanduser("~/Desktop/Master_Data/TN_Statewide"))
    p_pull.add_argument("--no-geometry", action="store_true")

    p_folder = sub.add_parser("pull-folder", help="download every layer in every service of a folder")
    p_folder.add_argument("url")
    p_folder.add_argument("--where", default="1=1")
    p_folder.add_argument("--fields", default="*")
    p_folder.add_argument("--outdir", default=os.path.expanduser("~/Desktop/Master_Data/TN_Statewide"))
    p_folder.add_argument("--no-geometry", action="store_true")

    args = ap.parse_args()
    if args.cmd == "inspect":
        inspect_url(args.url)
    elif args.cmd == "pull":
        pull_layer(args.url, args.name, args.where, args.fields, args.outdir, args.no_geometry)
    elif args.cmd == "pull-folder":
        pull_folder(args.url, args.outdir, args.where, args.fields, args.no_geometry)


if __name__ == "__main__":
    sys.exit(main())
