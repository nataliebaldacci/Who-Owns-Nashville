# WHO OWNS NASHVILLE — MASTER FILE

**The single authority.** One page that says which plan, which numbers, which
files, and which colors win. Consolidated 2026-07-13 from the Series Master
Plan (2026-07-06), the full project audit (2026-07-13), the canonical-universe
reconciliation (2026-07-13), and the locked palette. Supersedes all scattered
outlines and the May 2026 numbering. When another document disagrees with this
one, this one wins; fix the other document.

---

## 1. THE SERIES

**Organizing idea.** A home moves through a lifecycle: capital finances the
land, a developer banks it, a builder raises the house, an owner holds it, a
landlord rents it. The series walks the lifecycle backwards and reads each
stage against the 21st Century ROAD to Housing Act. The ban lands downstream;
the exceptions bless the upstream; land is the statute's blind spot; finance
cuts across everything.

| # | Part | Lifecycle role |
|---|---|---|
| I | Who Owns Nashville? | The cast and the framework. The finished, owned house. |
| II | Who Rents Nashville? | The end state; the activity the ban targets. |
| III | Who Builds Nashville? | The construction carve-out. |
| IV | Who Landbanks Nashville? | The Act's blind spot. Land before a "home" exists. |
| V | Who Finances Nashville? | The capital; securitized single-family rent. |

Introduction and Conclusion are unnumbered bookends. Every part uses the same
shape: Introduction → Background (+ Common Issues) → Framework (the Act) →
Research Scope → Methods/Datasets → Findings.

## 2. THE ACT (enrolled numbering — always cite these)

H.R. 6644, enrolled text:
`https://www.govinfo.gov/content/pkg/BILLS-119hr6644enr/html/BILLS-119hr6644enr.htm`

- **§1001(a)(2)** Excepted purchase: (A) build/convert-for-sale, (B)
  build-to-rent, (C) renovate-to-rent (≥15%), (D)–(E) homeownership/first-look,
  (F) debts previously contracted, (G) loss mitigation, (H) buy from compliant
  investor, (I) 2-year window, (J) 55+, (K) combinations.
- **§1001(a)(3)** Large institutional investor: ≥350 single-family homes;
  (B) investment-control tests; (B)(iv) >25% equity unless passive investor.
  **"Passive investor" is undefined in the enrolled text — a drafting gap and
  a finding.**
- **§1001(a)(4)** Purchase (mergers, foreclosures, bulk, construction).
- **§1001(a)(5)** Single-family home: ≤2 dwelling units; manufactured excluded.
- **§1001(b)** the prohibition · **(c)** renter outreach · **(d)** enforcement
  ($1M or 3× price) · **(f)** effective 180 days; sunset 15 years.

⚠ Old drafts and the live funnel page cite single-family as (a)(3) and
investor as (a)(4). That is the pre-enrollment numbering. **Flip to enrolled
everywhere: single-family = (a)(5), large investor = (a)(3).**

## 3. DATA UNIVERSES (full spec: `UNIVERSE.md`; code: `canonical_universes.py`)

Three universes; every dataset belongs to exactly one. Three measures; the same
code applies to any universe.

| Universe | Definition | Count |
|---|---|---|
| **U1 framework** | DUCOUNT 1–2 + LUDESC in ('NULL','SINGLE FAMILY','ZERO LOT LINE','DUPLEX','RESIDENTIAL CONDO') + FeatureType not multistory-condo/common/open-space | **205,933** |
| **U2 developable** | U1 use-list ∪ `LUDESC LIKE 'VACANT%'` (catches the county's VACANT RESIENTIAL misspelling), DUCOUNT relaxed | BTR / landbank maps |
| **U3 deeds** | every ParcelHistory deed event | **1,641,434** (corporate: 199,158) |

Measures: **M1** owner type (entity keyword test minus gov/trust; word-boundary
tokens — ' HUD ' and ' BANK ' bugs are fixed with regression tests);
**M2** ZIP-match occupancy + Davidson ZIP set + out-of-state; **M3** operator
attribution via the shell-resolution chain. **Vocabulary rule: "corporate /
entity-owned" = M1; "institutional" = M3 attributed operators only. Never mix.**

**Ground truth (live county query, 2026-07-13):** 286,721 parcels · framework
205,933 · dwelling units 215,041 · non-owner-occ 42,631 · out-of-state 11,929 ·
entity-owned 16,615. Pages built on their own pulls may drift ±1–2; label the
pull date instead of silently disagreeing.

## 4. CANONICAL FILES (which file wins)

| Question | File |
|---|---|
| U1 file of record | `Key_datasets/Nashville_Framework_Homes_CANONICAL_2026-07-07.parquet` (206,067 rows; use `owner_type_canonical`, NOT `owner_type`) |
| All current parcels | `08_Reference_Library/Parcels_Enriched/MASTER_Current_Parcels_FINAL_2026-05-28.csv` |
| Ownership master | `Key_datasets/Ownership_History_Enriched_Cleaned_2026-07-11_txntier.parquet` |
| Event history | `MASTER_Davidson_Parcel_Timeline_v5.parquet` (7,029,713 events) |
| Owner rollup (site) | `holdings_data.js` — 77 buckets, 8,923 parcels, no double-counting |
| BTR footprint | `BTR_Current_vs_Pipeline.geojson` — 3,494 (2,326 pipeline + 1,168 built) |
| Securitized parcels | `SEC_Pipeline/entity_parcel_ownership.csv` — 1,833 distinct parcels |
| Vacant universe | `Currently_Vacant_Parcels_CLEANED_2026-06-24.csv` — 28,418 (zoning filter, not LUDesc) |
| Evictions | `All_Evictions_MASTER_PARENTCLEAN_2026-06-30.csv` |
| Citations | `_URL_DATABASE.md` (16,744 URLs) |
| Retired parcels | `ParcelService_dump/` — exists nowhere else; never delete |

## 5. NUMBERS — USE / NEVER USE

**Use:** framework 205,933 · entity-owned 16,615 (state the token list) ·
BTR 3,494 (two-thirds pipeline: 2,326/3,494 = 66.6%) · securitized 1,833 ·
landbank vehicles seventeen / 1,444 parcels · enforcement citations 2,300 ·
registrations 30,014 · evictions Progress/Amherst/AMH = 886/619/9 ·
builder leaderboard NVR 6,212 / Beazer 4,911 / Pulte 2,680 / D.R. Horton 2,053
(permits, consolidated rollup).

**Never use:** ~~4,194 securitized~~ (mislabeled portfolio column, 2.3× high) ·
~~$220.8B principal~~ (double-counted; recompute from `is_main_row == True`) ·
~~24.2% public-builder share~~ (denominator exists in no file; reproducible is
20.1%) · ~~20,045 / 20,044 / 23,648 as "institutional"~~ (broad pre-framework
corporate cuts; pages now labeled) · ~~28,940 / 21,421 / 9,096 vacant~~ (April
LUDesc vintage; use 28,418 / 23,209 / 8,838) · ~~3,187 BTR~~ (community subset)
· ~~1,730 recordings / 904 borrowers~~ (DOT master holds 10,255 / 1,729).

**Unresolved (pick one + as-of date before publishing):** per-operator holdings
(Progress alone has seven competing values). Denominator + date on every table.

**Open verification:** the 1.47× burdened-tract concentration (Part I headline)
must be re-run on the canonical framework (`rerun_burdened_tract_finding.py`).
The "exclusively primary government data" claim is false until the Builty
dependency in Part II is purged or the claim is amended.

## 6. CAST (attribution targets for M3)

**Operators:** Progress (Pretium/Goldman), Invitation (INVH), American Homes 4
Rent, Tricon (Blackstone, +HPA), Amherst/Main Street Renewal, FirstKey
(Cerberus), VineBrook (NexPoint), Maymont (Brookfield), Bluerock, My Community
Homes (KKR), Yamasa. **Builders:** D.R. Horton, Lennar, NVR/Ryan,
Pulte/Centex, Toll, Meritage, KB, LGI, Century, Beazer; BTR: AMH; local: Ole
South, Normandy, Regent. **Landbankers:** Millrose, Walton Global, Rockpoint,
Arrived, Avenue One, Drapac, Kennedy Lewis, TPG AG, local OZ/LLC vehicles.
**Ultimate parents:** Pretium/Goldman, Blackstone, Cerberus, KKR.

## 7. SOURCES (all primary, all replayable)

| Source | Endpoint | Parts |
|---|---|---|
| Cadastral (current) | `maps.nashville.gov/arcgis/rest/services/Cadastral/Cadastral_Layers/MapServer/4` | I–II |
| ParcelHistory (deeds/permits/zoning/assessment) | `maps.nashville.gov/arcgis2/rest/services/Parcels/ParcelHistory/MapServer` | I–V |
| ParcelService (SOAP; genealogy, assessment history) | `maps.nashville.gov/ParcelService/Search.asmx?WSDL` | IV + verification |
| ePermits (registrations 176, res-new 20, STR 272 …) | `epermits.nashville.gov/api/permit/1.0/Case` | II–III |
| CaseLink (detainers) | `caselink.nashville.gov` | II |
| hubNashville 311 | ArcGIS FeatureServer | II |
| TN SOS entity search | `tncab.tnsos.gov` | I–V |
| SEC EDGAR | `sec.gov/edgar/search/` | II, V |
| Census/ACS | B25003/B25032 tenure, DP04 burden, S2504 | I–II |

## 8. STYLE + COLOR (locked)

- **Writing:** `Natalie_Writing_Style_Guide.md` governs anything with her name
  on it. Full paragraphs, active voice, short sentences, **no em dashes**, no
  hedging, no interpretive gloss. Citations: full URL + Bluebook, **no
  last-accessed dates.** Web maps: Montserrat navy/gold (`won-theme.css`);
  print: Garamond house style.
- **Palette** (`chart_cookbook/styles/locked_palette.py`, reference sheet
  `figures/locked_palette.png`): brand NAVY `#1c458c` + GOLD `#f0af1e`;
  operators = Prism_10 hand-assigned (**Progress red `#CC503E`, American Homes
  blue `#1D6996`**, Amherst teal, Starwood green, Tricon light-green,
  Invitation plum, VineBrook purple, Rithm orange, Brookfield gold, Regent
  dark-purple, unknown grey `#c9ced6`); generic series Prism_10; sequential
  SunsetDark_7 (institutional) / YlOrRd_6 / Blues_6 (tenure) / BuPu_6 (burden);
  diverging Geyser_7 / RdBu_9. Use `op_color(name)` and `ramp(role)`.
- **Charts:** `chart_cookbook/` (98 scripts + `cookbook_index.html` gallery).
  Every map/figure states its cut: **Universe + Measure + as-of date.**

## 9. OPEN ITEMS (in order)

1. **Rotate the Datawrapper token** (pasted in chat in June, never rotated).
2. **Re-run the 1.47× finding** on CANONICAL (`rerun_burdened_tract_finding.py`). Part I waits on it.
3. Re-run SEC_Pipeline post-2026-07-12 fix; mark the July 11 finance memo SUPERSEDED.
4. Triage Builty; settle the "exclusively primary data" claim.
5. Re-derive the public-builder share with a saved denominator.
6. Apply the §1001 enrolled renumbering on the live funnel page and Framework docx.
7. Rewrite the local CLAUDE.md against this file; restore the style gate (validator paths moved).
8. Re-cut the tract/blockgroup choropleths from CANONICAL (`recut_choropleth_aggregates.py`); regenerate site GeoJSONs.
9. Housekeeping: delete the 0-byte `Currently_Vacant_Parcels_CLEANED_withParent_2026-06-24.csv`, the 7 `~$` lock files, 22 `.bak`, 6 "Copy of"; rename `" STAR 2022 "`; remove the 77 MB Chrome profile from `TN_Bus_Lookup/_scraper/`.
