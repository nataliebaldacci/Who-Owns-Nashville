# Single-Family Definition & Year-Built Timeline — Methodology

**Author:** Natalie Baldacci, Vanderbilt Law School
**Map:** `SF_YearBuilt_Timeline_Nashville.html` (data: `Davidson_SF_YearBuilt_Timeline.geojson`)
**Scope:** How Davidson County's single-family housing stock was defined, classified by structure type, and dated by year built. All primary government data.

---

## 1. The single-family definition

The universe follows the **federal definition** of a single-family home in *Homes Are For People, Not Corporations*, H. Res. 1299, 119th Cong. tit. X § 1001(3), https://www.govinfo.gov/content/pkg/BILLS-119hres1299ih/html/BILLS-119hres1299ih.htm:

> A "single-family home" (A) means a structure that contains **2 or fewer dwelling units** that are each intended for residential occupancy by a single household; and (B) **does not include a manufactured home**.

Operationalized against the Davidson cadastral / CAMA layers as:

**KEEP:** `DUCount` is 1 or 2.

**EXCLUDE (three filters):**
1. **Manufactured / mobile homes** — `LUDesc` matching `MOBILE` or `MANUFACTURED` (MOBILE HOME, MOBILE HOME PARK). Per § 1001(3)(B).
2. **Multistory condo complexes** — `FeatureType` matching `MULTI` (Multistory Condo, Multistory Common Area). **18,069 parcels removed.** These are high-rise/large complexes, not the smaller 1–2 unit homes the definition targets; including them would add tens of thousands of stacked units.
3. **Non-residential structures** — `LUDesc` matching office, church, retail, shop, school, dormitory, auto, warehouse, medical, day-care, etc. (818 parcels). The federal text requires "residential occupancy," so a structure whose primary use is non-residential is excluded even if it carries a dwelling-unit count.

A valid assessor year built (1800–2027) and coordinates are also required for mapping.

**Result: 206,285 single-family parcels.**

---

## 2. Structure-type classification

Within the single-family universe, each parcel is one of three types (precedence order):

| Type | Rule | Count |
|---|---|---:|
| **Attached** (condo / townhome) | `LUDesc IN ('RESIDENTIAL CONDO','ZERO LOT LINE')` or `FeatureType = 'Condo'` | 43,231 |
| **Duplex / 2-unit** | not Attached, and (`DUCount = 2` or `LUDesc = 'DUPLEX'`) | 9,056 |
| **Detached** | everything else (single-family on a lot, 1 unit) | 153,998 |

Note: *zero lot line* is a home built on/near the property line, typically sharing a wall — the townhome / horizontal-property product — so it groups with Attached, not Detached.

---

## 3. Year built

Year built is taken from the primary assessor card (`YearBuilt_1`, 99.8% coverage on DUCount 1–2 parcels), falling back to the cadastral `yearbuilt`. The timeline places each home in its build year and accumulates 1900 → 2024 (homes built before 1900 appear at the 1900 floor).

Decade build-out (all single-family): 1920s 5,538 · 1930s 8,602 · 1940s 11,199 · **1950s 25,646** · 1960s 24,687 · 1970s 18,611 · **1980s 25,121** · 1990s 19,788 · **2000s 28,366** · 2010s 23,458 · 2020s (through 2024) 13,868.

---

## 4. Owner-occupancy (carried for a later layer)

Each parcel also carries an `oo` flag — owner-occupied when the owner mailing zip equals the property zip (`OwnZip = PropZip`), the project's standard absentee-owner proxy. Current split: **owner-occupied 79.3% / non-owner-occupied 20.7%.** (A future version will refine this with a dedicated occupancy source.)

---

## 5. Data sources

- **Parcels with Building Characteristics (CAMA)** — `https://services2.arcgis.com/HdTo6HJqh92wn4D8/ArcGIS/rest/services/Parcels_with_Building_Characteristics_view/FeatureServer/0` (StructureType, YearBuilt, FinishedArea, AssessorCardNumber, by APN).
- **Cadastral / Ownership Parcels (Layer 4)** — `https://maps.nashville.gov/arcgis/rest/services/Cadastral/Cadastral_Layers/MapServer/4` (LUDesc, DUCount, FeatureType, owner/property addresses, appraisal).
- **Building Footprints** — `https://services2.arcgis.com/HdTo6HJqh92wn4D8/ArcGIS/rest/services/Building_Footprints_view/FeatureServer`.
- Local masters: `MASTER_Current_Parcels_FINAL_2026-05-28.csv`, `Full_Parcels_Character_Flat.csv`, `Merged_Footprints_FINAL_20260213…geojson`.

All Davidson County. A reader can replay any layer above to reproduce the universe.
