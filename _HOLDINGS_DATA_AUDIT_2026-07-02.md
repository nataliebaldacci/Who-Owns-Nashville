# holdings_data.js audit — 2026-07-02

Source: `window.HOLDINGS` in `_WhoOwnsNashville_Maps_Site/holdings_data.js` (live, commits b275897 + 866bbfe, both 2026-07-02).

## Headline
- 8,988 distinct parcels across 97 operator buckets.
- **943 parcels are double-/triple-counted** (appear in >1 bucket).
- **37 owners sit in multiple buckets.**
- Root cause: build script grouped owners by loose name-matching, creating (a) a junk "brookfield" bucket and (b) duplicate operator buckets for the same operator.

## Problem 1 — "brookfield" bucket is a junk drawer (368 parcels, 18 owners)
Only ~16 parcels are genuinely Brookfield-family. Remove these misfiled owners:
- VB TAH, LLC (106) → VineBrook / NexPoint
- CORE PBSFR NASHVILLE HERRON, LLC (96) → Core Spaces / PBSFR
- RESIDENTIAL HOME BUYER NASHVILLE, LLC (74) + E NASHVILLE (1) → NOT Brookfield (E NASHVILLE also in progess_res)
- 404/410/413 WEST BROOKFIELD TRUST, O.I.C. BROOKFIELD COTTAGES/CONDOMINIUMS (5) → street addresses named "Brookfield", coincidental match
- ASHTON NASHVILLE RESIDENTIAL, LLC (1) → Ashton Woods (has own bucket)
KEEP: BROOKFIELD HOLDINGS (CANE RIDGE) 64 (verify), CONREX ML 9, BSFR 6, BNTR 3, AG BROOKFIELD 2.

## Problem 2 — duplicate operator buckets (same operator, two keys)
Merge each pair (they share the same parcels):
- core + core_pbsfr  (Core Spaces / PBSFR)
- vinebrook + vb_tah_llc_nextpoint  (VineBrook / NexPoint)
- lennar + lennar_homes  (Lennar)
- rsd + rsd_dev  (RSD)
- kllb + kllb_aiv_llc_kennedy_lewis  (KLLB / Kennedy Lewis)
- clayton_prop ↔ domaintimberlake  (Domain Timberlake Multistate 2 — belongs to Domain, wrongly also in Clayton)

## Problem 3 — CPI/Amherst wrongly in AMH
CPI/AMHERST SFR PROGRAM [II] OWNER LLC (many spacing variants) appears in BOTH american_homes_4_rent and amherst. It is Amherst. Remove from AMH.
Also: name-variant duplication (spacing) treats one entity as several owners.

## Status
- Nothing fixed/pushed yet. Awaiting Natalie's decision on fix scope.
- All misfiled parcels verified present in their correct buckets, so removing duplicates loses no parcels.
