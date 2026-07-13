# Who Owns Nashville — Canonical Data Universes

One page that defines every dataset cut. Each map declares a **universe** (which
parcels/records) and a **measure** (how they are split). The machine-readable
version of this file is `canonical_universes.py`; the narrative methodology
lives in `Data_Filter_Funnel.html`, `Historical_Owners.html`, and
`Methodology_Corporate_Landlords.html`.

Snapshot of record: **July 6, 2026** (cadastral pull; 286,710 of 286,721 live
parcels captured, 11 recently retired).

---

## Stage 1 — Source (shared)

| Source | Endpoint | Records |
|---|---|---|
| Current cadastral | `maps.nashville.gov/arcgis/rest/services/Cadastral/Cadastral_Layers/MapServer/4` | 286,721 parcels |
| Ownership history | `maps.nashville.gov/arcgis2/rest/services/Parcels/ParcelHistory/MapServer/2` | 1,641,434 deed events |
| Parcel service (SOAP) | `maps.nashville.gov/ParcelService/Search.asmx?WSDL` | per-parcel enrichment |

The Parcel Service is **not a universe** — it is the verification layer:
assessment history, building characteristics, and sales detail pulled per APN to
cross-check values coming out of U1–U3 (e.g., assessed-value trajectories for
operator-held homes, year-built confirmation for the BTR lifecycle split).

## Stage 2 — Universes (fork; every dataset belongs to exactly one)

### U1 · `framework` — existing 1–2-unit homes (21st Century Housing Act)
The current-owners universe. Verbatim county where-clause:

```sql
(ducount = 1 OR ducount = 2)
AND ludesc IN ('NULL','SINGLE FAMILY','ZERO LOT LINE','DUPLEX','RESIDENTIAL CONDO')
AND featuretype NOT IN ('Multistory Condo','Multistory Common Area','Open Space')
```

Expected count: **205,933 parcels**. Note the county stores unclassified land
use as the literal string `'NULL'` — the filter matches that string, it is not
SQL `IS NULL`. Never apply the `ludesc` list without the `ducount` condition.

Feeds: current-ownership maps, institutional-rate choropleths, tenure,
cost-burden, eviction maps.

### U2 · `developable` — BTR / land-banking universe
Everything in U1 **plus vacant land**, because build-to-rent and land-banking
analysis must see parcels before homes exist:

```sql
(   -- built homes (U1 use-type list)
    (ducount = 1 OR ducount = 2)
    AND ludesc IN ('NULL','SINGLE FAMILY','ZERO LOT LINE','DUPLEX','RESIDENTIAL CONDO')
) OR (
    -- vacant / pre-development (ducount may be 0)
    ludesc LIKE 'VACANT%'
)
AND featuretype NOT IN ('Multistory Condo','Multistory Common Area','Open Space')
```

`LIKE 'VACANT%'` is deliberate: it captures VACANT RESIDENTIAL LAND, VACANT
RURAL LAND, VACANT ZONED MULTI FAMILY, VACANT COMMERCIAL LAND **and the county's
misspelling `VACANT RESIENTIAL LAND`** (present on ~60 parcels). Exact-match
lists silently drop the misspelled rows.

Lifecycle within U2 is labeled by `status`: `Current (built home)` vs
`Pipeline (vacant / in development)` (see `BTR_Lifecycle_Polygons.geojson`).

Feeds: BTR lifecycle/pipeline/machine maps, land-banking, plat/subdivision maps.

### U3 · `deeds` — historical transaction universe
One row per **deed event**, not per parcel: every entity that ever took title.
Source: ParcelHistory MapServer/2, 1,641,434 events, 2001–present including
foreclosures. Corporate test (below) applied to the deed record yields
**199,158 corporate-entity deed events**.

Feeds: acquisition timelines, historical-owner rankings, deed/foreclosure maps.

---

## Stage 3 — Measures (shared; apply identically to any universe)

### M1 · Ownership type
Categories: Individual / **Entity** / Trust / Bank–Lender / Government.
An owner name is an entity when it carries a business token and is not a
government body or trust. **Canonical token list (the Historical_Owners
superset — use this one going forward):**

```
LLC, LLP, ' LP', L.P, ' INC', CORP, LTD, LIMITED, ' CO ', 'CO.', COMPANY,
PARTNER, ASSOC, HOMES, HOLDING, CAPITAL, INVEST, FUND, SOLUTION, SFR,
ASSET, BORROW, ' JV'
```
minus government (CITY OF, HOUSING AUTH, METRO…GOV, STATE OF, COUNTY OF, HUD,
MDHA, UNITED STATES) minus trusts (TRUST, REVOCABLE, LIVING TR, FAMILY TR).

> ⚠ Known drift: the funnel page's live query uses a 15-token subset (no LLP,
> LIMITED, CO, ASSOC, FUND, SOLUTION, ASSET). Expected counts below cite the
> query that produced them; new cuts should use the canonical list.

Expected (U1, July 6 2026): Individual 172,407 · Entity **16,769** · Trust
16,188 · Bank/Lender 161 · Government 408.

### M2 · Occupancy & geography (ZIP-match proxy)
- **Owner-occupied**: owner mailing ZIP = parcel ZIP. Absentee otherwise.
- **Out-of-county**: mailing ZIP outside the Davidson set
  `37013, 37072, 37076, 37080, 37115, 37138, 37189, 37201–37221, 37228`.
- **Out-of-state**: `StateCode <> 'TN'`.

Expected (U1): non-owner-occupied 42,632 · out-of-state 11,929.
Applied to U3 the same way (e.g., 126,649 out-of-state deed records).

### M3 · Operator attribution
The shell-resolution chain (known-shell patterns → Security-for-Sale crosswalk
→ canonical owner→operator crosswalk → name-pattern rules → address clustering
→ TN SOS registry). Documented in `Methodology_Corporate_Landlords.html`.
Yields **institutional** (attributed to a named operator) vs **other corporate**
(entity, unattributed).

**Vocabulary rule:** "entity-owned / corporate" = M1. "Institutional" = M3
attributed operators ONLY. Never label an M1 count as institutional.

---

## Map badge convention

Every map/page states its cut in one line, e.g.:

> Universe: `framework` (205,933 homes, July 6 2026) · Measure: entity-owned (M1)

> Universe: `developable` · Measure: operator-attributed (M3), lifecycle split

> Universe: `deeds` (1,641,434 events) · Measure: corporate (M1) × out-of-state (M2)

---

## Reconciliation findings (2026-07-13, baseline vs county)

Run against `Nashville_Framework_Homes_BASELINE_2026-07-07.parquet` (225,471
rows), the gap to the county's 205,933 decomposed fully:

1. **18,071 rows fail the FeatureType exclusion** — 18,064 Multistory Condo
   (land-use: 18,025 Residential Condo). DUCOUNT dropped **zero** rows: the
   baseline was already DUCOUNT-filtered.
2. **~1,333 rows carry land uses outside the 5-value list** (Mobile Home 407,
   Office 319, Rural Combo 77, Dormitory 76, …) — the baseline never applied
   the LUDESC list. Applying the FULL clause locally yields **206,067**;
   the ~134 remaining vs 205,933 is one-day snapshot drift. No duplicates.
3. **Legacy "20,045" explained**: Corporate counted on the broad universe
   (20,873 at this vintage). One filter vintage, not a data error.
4. **Classifier fixes** (both sides had bugs; canonical corrected in
   `canonical_universes.py` with regression tests from real disagreements):
   canonical had `HUD`→HUDSON and `BANK`→BANKS substring hits and missed
   `SECRETARY OF …`; the file's `owner_type` sent community-property trusts to
   Corporate (1,196), missed `REV LIVING TR` variants (756) and
   LP/ASSOC/PLLC entities (182), and hit `LOAN` inside surnames (23).

Derivation of the U1 file of record from the baseline:
`derive_canonical_framework.py` → `Nashville_Framework_Homes_CANONICAL_*.parquet`
(full clause + fixed-classifier `owner_type_canonical` column).

**MATERIALIZED 2026-07-13.** `Nashville_Framework_Homes_CANONICAL_2026-07-07.parquet`:
**206,067 rows** (county July-6 query 205,933; +134 = one-day snapshot drift).
Land use: SF 156,644 · Res Condo 36,936 · Duplex 7,068 · Zero Lot Line 5,419.
Owner split (fixed canonical classifier): Individual 173,132 · **Entity 16,567**
· Trust 15,944 · Government 377 · Bank-Lender 47. Deltas vs the funnel's
published split (172,407/16,769/16,188/408/161) are classifier residue — the
funnel used the 15-token list and a looser bank test that counted BANKS-surname
individuals. **The canonical parquet's numbers are authoritative for local
work; regenerate the funnel page's split from it at the next site update.**

## Known legacy cuts to reconcile (pre-dating this spec)

| Dataset / page | Cut it used | Issue |
|---|---|---|
| `Davidson_Institutional_Pct_by_Tract.geojson` (224,322 res / 34,269 "inst") | LUDESC list only, no DUCOUNT/featuretype exclusions; numerator is M1 broad keyword | re-cut on U1; relabel numerator "entity-owned" or re-cut as M3 |
| `institutional_by_blockgroup.geojson` (232,863 res / 4,516 inst) | different denominator again; numerator is M3 | re-cut denominator on U1 |
| `Davidson_Corporate_Parcel_Shapes.geojson` + `Davidson_Corporate_Timeline.geojson` (18,888) | internally consistent pair; superset of U1×M1 (16,769) | document or re-cut |
| `data/citywide_corp.json` (38,417 incl 33,590 other) | app universe, broader than U1 | document universe on the app map |
| `Corporate_Landlords_by_CouncilDistrict.html`, `Landlord_Permit_DataFlow.html`, `WhoOwnsNashville_Explorer.html` | embed legacy count 20,045 | patch to U1 numbers |
