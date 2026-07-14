#!/usr/bin/env python3
"""Dedupe ownership-history rows in parcel_history/*.json.gz.

Source layer: maps.nashville.gov/arcgis2 Parcels/ParcelHistory/MapServer/2
(Ownership History). Each shard maps parcel ID -> {own, per, zon}; an `own`
row is [Owner, AcqDate, MailAddress, SalePrice, Status, InstrumentType,
Instrument].

Two duplicate shapes are removed, per parcel:

1. Exact duplicates - identical rows repeated verbatim.
2. Same-instrument variants - the recording instrument number (e.g.
   "DB-20190304 0019443") identifies one deed, so rows in the same parcel
   sharing a non-empty instrument are the same event when their owner names
   are the same or near-variants (truncations like "RODRIGUEZ, V" vs
   "RODRIGUEZ, VLADAMIR S. U.", punctuation/typo variants like "NVR, INC."
   vs "NVR INC"). Rows sharing an instrument but naming genuinely different
   parties (life estates, multi-party conveyances) are kept.

Merge rules within a group: base row is the Active one if present (that is
the assessor's current record), else the first in chain order; the longest
owner spelling wins (undoes truncation); empty address/price/date fields are
filled from the other rows; status is Active if any row was Active, so the
one-Active-row-per-parcel invariant is preserved. The merged row keeps the
chain position of the group's first occurrence.

Usage: python3 dedupe_parcel_history.py [--apply]
Without --apply it is a dry run that only prints statistics.
"""
import collections
import difflib
import glob
import gzip
import io
import json
import os
import re
import sys

OWNER, DATE, ADDR, PRICE, STATUS, INSTTYPE, INSTRUMENT = range(7)


def norm_name(s):
    return re.sub(r'\s+', ' ', re.sub(r'[^A-Z0-9 ]', '', s.upper())).strip()


def same_owner(a, b):
    """True when two owner strings are variants of the same name."""
    na, nb = norm_name(a), norm_name(b)
    if na == nb:
        return True
    shorter, longer = sorted((na, nb), key=len)
    # Truncated field: the shorter is a prefix of the longer.
    if shorter and longer.startswith(shorter):
        return True
    return difflib.SequenceMatcher(None, na, nb).ratio() >= 0.75


def merge_group(rows):
    base = next((r for r in rows if r[STATUS] == 'Active'), rows[0])
    merged = list(base)
    merged[OWNER] = max((r[OWNER] for r in rows), key=len)
    for i in (DATE, ADDR, PRICE):
        if not merged[i]:
            merged[i] = next((r[i] for r in rows if r[i]), merged[i])
    if any(r[STATUS] == 'Active' for r in rows):
        merged[STATUS] = 'Active'
    return merged


def dedupe_chain(own):
    """Return (new_chain, n_exact_removed, n_merged_removed)."""
    # Pass 1: exact duplicates.
    seen = set()
    chain = []
    exact = 0
    for r in own:
        t = tuple(r)
        if t in seen:
            exact += 1
            continue
        seen.add(t)
        chain.append(list(r))

    # Pass 2: same-instrument groups, connected by owner-name similarity.
    by_inst = collections.defaultdict(list)
    for idx, r in enumerate(chain):
        if r[INSTRUMENT].strip():
            by_inst[r[INSTRUMENT]].append(idx)

    drop = set()
    replace = {}
    for inst, idxs in by_inst.items():
        if len(idxs) < 2:
            continue
        # Cluster the group's rows into connected components of name variants.
        remaining = list(idxs)
        while remaining:
            comp = [remaining.pop(0)]
            changed = True
            while changed:
                changed = False
                for j in remaining[:]:
                    if any(same_owner(chain[j][OWNER], chain[k][OWNER]) for k in comp):
                        comp.append(j)
                        remaining.remove(j)
                        changed = True
            if len(comp) > 1:
                comp.sort()
                replace[comp[0]] = merge_group([chain[k] for k in comp])
                drop.update(comp[1:])

    out = []
    for idx, r in enumerate(chain):
        if idx in drop:
            continue
        out.append(replace.get(idx, r))
    return out, exact, len(drop)


def main():
    apply = '--apply' in sys.argv
    root = os.path.dirname(os.path.abspath(__file__))
    files = sorted(glob.glob(os.path.join(root, 'parcel_history', '*.json.gz')))
    tot_exact = tot_merged = tot_rows = changed_files = 0
    changed_parcels = 0
    for path in files:
        with gzip.open(path, 'rt', encoding='utf-8') as fh:
            shard = json.load(fh)
        dirty = False
        for pid, rec in shard.items():
            own = rec.get('own') or []
            tot_rows += len(own)
            if len(own) < 2:
                continue
            new, exact, merged = dedupe_chain(own)
            if exact or merged:
                tot_exact += exact
                tot_merged += merged
                changed_parcels += 1
                rec['own'] = new
                dirty = True
        if dirty:
            changed_files += 1
            if apply:
                buf = io.BytesIO()
                # mtime=0 keeps the gzip output deterministic across runs.
                with gzip.GzipFile(fileobj=buf, mode='wb', mtime=0) as gz:
                    gz.write(json.dumps(shard, separators=(',', ':')).encode('utf-8'))
                with open(path, 'wb') as fh:
                    fh.write(buf.getvalue())

    mode = 'APPLIED' if apply else 'DRY RUN'
    print(f'[{mode}] shards: {len(files)}  own rows: {tot_rows}')
    print(f'exact duplicate rows removed: {tot_exact}')
    print(f'same-instrument variant rows merged away: {tot_merged}')
    print(f'parcels touched: {changed_parcels}  shards touched: {changed_files}')


if __name__ == '__main__':
    main()
