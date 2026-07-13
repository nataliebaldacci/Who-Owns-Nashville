"""Inventory EVERY dataset in Key_datasets and bundle small samples for upload.

RUN (copy-paste, no edits needed):

    cd /Users/nataliebaldacci/Master_Data/Nashville/Key_datasets
    python3 scan_key_datasets.py

It scans this folder and the data/ subfolder for .parquet and .csv.xz files and
writes ONE small file:

    key_datasets_bundle.zip     (usually a few MB)

containing an inventory (file, size, rows, full schema) plus a 200-row sample
of every dataset. Upload key_datasets_bundle.zip back into the chat.

Needs: pandas + pyarrow  (pip3 install pandas pyarrow  if missing).
Big files are never fully loaded — parquet row counts come from file metadata.
"""
import os, sys, json, glob, zipfile, tempfile, traceback

SAMPLE_ROWS = 200


def scan_parquet(path):
    import pyarrow.parquet as pq
    import pandas as pd
    pf = pq.ParquetFile(path)
    meta = {
        "rows": pf.metadata.num_rows,
        "columns": {f.name: str(f.physical_type) for f in pf.schema},
        "n_columns": pf.metadata.num_columns,
    }
    # sample = first batch only (never loads the whole file)
    batch = next(pf.iter_batches(batch_size=SAMPLE_ROWS))
    sample = batch.to_pandas()
    return meta, sample


def scan_csv_xz(path):
    import pandas as pd
    sample = pd.read_csv(path, compression="xz", nrows=SAMPLE_ROWS, low_memory=False)
    meta = {
        "rows": None,   # counting would decompress the whole file; skipped
        "columns": {c: str(t) for c, t in sample.dtypes.items()},
        "n_columns": len(sample.columns),
    }
    return meta, sample


def main():
    root = os.getcwd()
    targets = sorted(
        glob.glob(os.path.join(root, "*.parquet"))
        + glob.glob(os.path.join(root, "data", "*.parquet"))
        + glob.glob(os.path.join(root, "*.csv.xz"))
        + glob.glob(os.path.join(root, "data", "*.csv.xz"))
    )
    if not targets:
        sys.exit("No .parquet or .csv.xz files found here — run this from Key_datasets.")

    inventory = {}
    tmp = tempfile.mkdtemp()
    sample_files = []
    for path in targets:
        rel = os.path.relpath(path, root)
        size_mb = os.path.getsize(path) / 1e6
        print(f"scanning {rel}  ({size_mb:,.1f} MB) ...", flush=True)
        try:
            if path.endswith(".parquet"):
                meta, sample = scan_parquet(path)
            else:
                meta, sample = scan_csv_xz(path)
            meta["size_mb"] = round(size_mb, 1)
            inventory[rel] = meta
            sname = rel.replace(os.sep, "__").replace(".parquet", "").replace(".csv.xz", "") + "__sample.csv"
            spath = os.path.join(tmp, sname)
            sample.to_csv(spath, index=False)
            sample_files.append((spath, "samples/" + sname))
            rows = f"{meta['rows']:,}" if meta["rows"] else "?"
            print(f"   ok: {rows} rows, {meta['n_columns']} cols")
        except Exception as e:
            inventory[rel] = {"size_mb": round(size_mb, 1), "error": str(e)}
            print(f"   ERROR: {e}")
            traceback.print_exc(limit=1)

    inv_path = os.path.join(tmp, "inventory.json")
    json.dump(inventory, open(inv_path, "w"), indent=1, default=str)

    out = os.path.join(root, "key_datasets_bundle.zip")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(inv_path, "inventory.json")
        for spath, arc in sample_files:
            z.write(spath, arc)

    print(f"\nwrote {out}  ({os.path.getsize(out)/1e6:,.1f} MB)")
    print(">>> Upload key_datasets_bundle.zip into the chat.")


if __name__ == "__main__":
    main()
