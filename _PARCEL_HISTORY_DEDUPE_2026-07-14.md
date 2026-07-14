# Parcel History Ownership Dedupe — 2026-07-14

Independent dedupe pass over the local copy of the Assessor's **Ownership
History** layer (maps.nashville.gov/arcgis2 → Parcels/ParcelHistory/MapServer/2),
stored in `parcel_history/*.json.gz` and rendered as each parcel's Chain of
Title in `Data.html`. Script: `dedupe_parcel_history.py` (rerunnable;
`--apply` writes, otherwise dry run).

## Results

| Metric | Value |
| --- | ---: |
| Shards scanned | 313 |
| Parcels | 284,803 (unchanged) |
| Ownership rows before | 1,365,106 |
| Ownership rows after | 1,364,701 |
| **Duplicate rows removed** | **405** (0.03%) |
| — exact duplicate rows | 165 |
| — same-instrument variant rows merged | 240 |
| Parcels touched | 399 |
| Shards rewritten | 128 |

## What counted as a duplicate

**1. Exact duplicates (165 rows).** The identical row repeated verbatim in
one parcel's chain, e.g. parcel `044090B06800CO` listed
`FLORO, KRISTINA K / 02/19/2021 / DB-20210223 0022487` twice.

**2. Same-instrument variants (240 rows).** A recording instrument number
(`DB-20220621 0070117`) identifies one deed, so two rows in the same parcel
sharing an instrument are one event when the owner names match or are
near-variants. Observed corruption patterns, all collapsed:

- *Status pairs* — the same deed listed once `Active` and once `Inactive`
  (e.g. `MURPHY, DAVID`, `043100B10000CO`).
- *Truncated names* — `ELIZONDO, YASSEL MARTINEZ & RODRIGUEZ, V` vs
  `… RODRIGUEZ, VLADAMIR S. U.` (longest spelling kept).
- *Punctuation/typo variants* — `NVR, INC.` vs `NVR INC`;
  `GILLIAM` vs `GILLIIAM`.
- *Conflicting sale price* — `RECHTER` deed on `9113024100` appeared twice
  as `Active` with prices 834,626 and 834,000; this was the county's only
  parcel with two Active rows caused by duplication, now one.

**Merge rules:** base row is the `Active` one if present, else the first in
chain order; longest owner spelling wins; empty date/address/price fields are
filled from the other rows; merged status is `Active` if any row was Active.
Chain order is preserved (merged row keeps the first occurrence's slot).

## What was deliberately NOT merged

Rows sharing an instrument but naming genuinely different parties were kept —
these are real multi-party records, not duplicates:

- Life-estate and remainder interests (`FARLESS, MARGARET M.` +
  `SHOLEY, G. M. & FARLESS, M. M (LE)`, one Death Certificate instrument).
- Multi-party conveyances (`AON CONSTRUCTION, LLC` +
  `HUDDLESTON, TAURIS & ET AL` on one quit claim).
- Probable same-person-different-surname rows (`HOFFMAN, DEBBIE D.` vs
  `SIMPLER, DEBORAH D. H.`) — unverifiable without the deed image, kept.

A name-similarity guard (normalized comparison + prefix/edit-distance test,
threshold 0.75) makes this split; it was spot-checked against both lists
above with zero false merges and zero missed variants.

## Verification

- Parcel count unchanged (284,803); `per` (permits) and `zon` (zoning)
  arrays byte-identical before/after.
- The one-`Active`-row-per-parcel invariant held: no parcel's Active count
  changed except `9113024100` (2 → 1, the duplicated Active deed above).
- Zero residual exact duplicates or mergeable same-instrument variants
  after the pass.
- Shard JSON schema and gzip encoding unchanged, so `Data.html` needs no
  changes.

## Notes

- Live re-pull of MapServer/2 was not possible from this session (host
  blocked by the sandbox's network policy), so the pass ran on the committed
  local copy — which is the data the site actually serves.
- Out of scope but observed: the `zon` (zoning history) arrays contain 262
  exact duplicate rows; the `per` (permit) arrays contain none. Say the word
  and the same pass can cover zoning.
