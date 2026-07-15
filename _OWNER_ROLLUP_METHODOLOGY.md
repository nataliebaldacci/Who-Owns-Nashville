# Owner dedupe + rollup — methodology log (run 2026-07-15)

Pipeline: `owner_rollup_pipeline.py` · Inputs: `data/rollup_inputs/` ·
Outputs: `Owner_Rollup_Linked_20260715.csv`, `Owner_Groups_Summary_20260715.csv`

Replicates the record-linkage design of Hangen & O'Brien (2024) and the
service-address rule of Shelton & Seymour's *Horizontal Holdings* (2024),
substituting two Davidson-specific sources for Massachusetts corporate
filings: (1) landlord-registration **case_people** (every person on a Metro
landlord-registration case, with the real mailing address the law now
requires), and (2) the **TN Secretary of State** resolved-entity table
(principal office and mailing addresses; registered agents excluded as
service mills).

## Stage-by-stage counts

| Stage | Rule | Result |
|---|---|---|
| 0 | Current owner (Owner1) per parcel; corporate/trust name test | 324,748 parcels → 90,076 corporate/trust-owned |
| 1–2 | Clean/standardize names (punctuation, LLC/LP/CORP variants, misspellings); exact match | 39,804 raw names → 37,659 cleaned owners → 37,300 after suffix-stem linking |
| 3 | Fuzzy: char 3-gram TF-IDF cosine ≥ 0.85 (conservative, per H&O) | 4,860 pairs linked → 34,192 groups |
| 4 | Shared **non-hub** deed mailing address (2–8 distinct stems only) | 1,919 hub addresses excluded (C/O tax reps, agent mills, shared PO Boxes, any address with ≥12 stems); 5,474 links → 28,718 groups |
| 5 | TN SOS principal/mailing address of resolved entity (agents excluded) | 3,350 of 9,045 SOS stems matched; 89 links → 28,629 groups |
| 6 | Shared people from case_people — owner-side roles only (Property Owner, Permit Owner, Landlord Owner/Co-Owner); person key = name + mailing address; degree ≤ 10 entities | 689 linking people; 527 links → 28,102 groups |
| 7 | Connected components; canonical label prefers curated `canon_parent` names | **28,102 owner groups; 3,917 groups link 2+ names, covering 48,578 parcels** |

## Guards against false positives (the failure mode H&O warn about)

- Service/agent addresses never link: `C/O …`, Ryan LLC, CSC (2908 Poston
  Ave), CT Corporation (800 S Gay St), registered-agent mills, any PO Box
  shared by ≥6 stems, any address shared by ≥12 stems.
- Address links only act on small clusters (2–8 distinct name-stems).
- People are deduplicated by **name + mailing address**, not name alone
  (name-only linking chains common names), and only from owner-side roles —
  property managers, billing contacts, and permit applicants never link.
- A single weak link (one shared address or person) may not merge two
  portfolios that both already exceed 300 parcels.
- Groups with ≥40 member names are flagged `REVIEW` in the summary for
  manual audit rather than being trusted automatically — the papers' own
  practice, since no ground truth exists.

## Validation spot-checks

- **AH4R family**: 24 shell spellings (AH4R 1 TN / I TN / TN 11 / Properties
  Two…) → one group, 1,139 parcels, labeled by the curated parent.
- **Progress Residential**: 32 borrower-entity spellings and typos
  (PROGESS…, RESEDENTIAL…) → one group, 743 parcels.
- **Meritage**: `MERITAGE HOMES OF TENNESSE INC` (typo) merged with the
  correct spelling — 387 parcels.
- PO-Box hubs (e.g. `PO BOX 4900 C/O RYAN LLC`) correctly link **nothing**.

## Citations

- Hangen, F. & O'Brien, D.T. (2024). Linking Landlords to Uncover Ownership
  Obscurity. *Housing Studies*. doi:10.1080/02673037.2024.2325508
- Shelton, T. & Seymour, E. (2024). Horizontal Holdings: Untangling the
  Networks of Corporate Landlords. *Annals of the AAG* 114(8).
  doi:10.1080/24694452.2023.2278690
- Torres, A. (2024). Who Owns Our Homes: Methods to Group and Unmask
  Anonymous Corporate Owners. *Cityscape* (HUD).
- Immergluck, D. et al. (2020). Evictions, Large Owners, and Serial Filings.
  *Housing Studies* 35(5).
- Who Owns Atlanta (who-owns-atlanta.org) and MIT Spatial Action
  (whoownsmass-processing) reference implementations.
