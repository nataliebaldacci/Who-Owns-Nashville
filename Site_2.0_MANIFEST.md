# Site 2.0 manifest (built October 19, 2026)

This folder is the complete, deployable website: only what the seven finished papers cite, rebuilt or verified on the canonical July 2026 numbers. The old site folder `_WhoOwnsNashville_Maps_Site/` (164 HTML pages) is untouched and stays on disk; its pages also remain in the GitHub repository's history.

## Pages (10)
- Chilton_2018_Update.html
- Data_Filter_Funnel.html
- LandBank_Option_Agreements.html
- LandBank_Takedowns_Nashville.html
- LandBank_Timeline_Nashville.html
- Securitization_Deal_Map.html
- Securitization_Timeline_Map.html
- Securitized_Parcels_MAP_v2.html
- index.html
- landbanking-appendices.html

## Cited URL -> page (unchanged filenames, so no paper needs re-citing)
| URL cited in the papers | Status |
|---|---|
| /Chilton_2018_Update.html | REBUILT from Burdened_Tract_ReRun_CANONICAL_2026-07-15.csv + Tables_CANONICAL (was never pushed; old local copy carried 20,045 / 1,711 and eight PENDING blocks) |
| /Securitized_Parcels_MAP_v2.html | REPLACED by SEC_Pipeline/securitized_map.html (1,833 canonical parcels; the old page mapped the dead 4,194 set) |
| /Data_Filter_Funnel.html | copied; Historical_Owners link retargeted; 42,632 -> 42,631 |
| /LandBank_Option_Agreements.html, /LandBank_Timeline_Nashville.html, /LandBank_Takedowns_Nashville.html, /landbanking-appendices.html | copied unchanged (verified clean) |
| / (root) | new index: papers, exhibits, data appendix, method |

## Added
- Securitization_Deal_Map.html and Securitization_Timeline_Map.html (canonical SEC_Pipeline builds, not previously on the site).
- data/ (the online data appendix the papers cite; 28 files; see data/README.md).
- papers/ (the seven .docx finals; replace with PDFs at Phase 3).
- Chilton_Tracts_2026.geojson (174 tracts with canonical values); Davidson_County_Boundary.geojson served locally.

## Not carried over
156 old pages, including every page the July audit flagged for dead numbers (20,045 / 23,648 / 4,194 / 48.6% / 1.47x) and the holdings explorer that runs on the pre-grounding `holdings_data.js` (943 double-counted parcels). They are not deleted: the old folder and the git history keep them. Bring any one back only after it is regenerated on canonical numbers.

## Deploy (not yet done; needs Natalie's go-ahead)
Option A (recommended, keeps every cited URL): in the `Who-Owns-Nashville` repo, remove the tracked files from the working tree, copy this folder's contents in, commit as "Site 2.0: papers, cited exhibits, data appendix", push to main. GitHub Pages serves the same root, so https://nataliebaldacci.github.io/Who-Owns-Nashville/Chilton_2018_Update.html resolves for the first time. Old pages stay in history.
Option B: a new repository and URL root, which would require re-citing nine URLs across the papers. Not recommended.

## Build log
- copy _WhoOwnsNashville_Maps_Site/won-theme.css -> won-theme.css
- copy _WhoOwnsNashville_Maps_Site/favicon.svg -> favicon.svg
- copy _WhoOwnsNashville_Maps_Site/Davidson_County_Boundary.geojson -> Davidson_County_Boundary.geojson
- copy _WhoOwnsNashville_Maps_Site/LandBank_Timeline_Nashville.html -> LandBank_Timeline_Nashville.html
- copy _WhoOwnsNashville_Maps_Site/Davidson_LandBank_Timeline.geojson -> Davidson_LandBank_Timeline.geojson
- copy _WhoOwnsNashville_Maps_Site/LandBank_Takedowns_Nashville.html -> LandBank_Takedowns_Nashville.html
- copy _WhoOwnsNashville_Maps_Site/Davidson_LandBank_Takedowns.geojson -> Davidson_LandBank_Takedowns.geojson
- copy _WhoOwnsNashville_Maps_Site/LandBank_Option_Agreements.html -> LandBank_Option_Agreements.html
- copy _WhoOwnsNashville_Maps_Site/landbanking-appendices.html -> landbanking-appendices.html
- patch Data_Filter_Funnel.html: Historical_Owners link -> index#data; 42,632 -> 42,631
- copy SEC_Pipeline/securitized_map.html -> Securitized_Parcels_MAP_v2.html (boundary fetch made local); replaces the 4,194-parcel v2 page
- copy SEC_Pipeline/securitization_deal_map.html -> Securitization_Deal_Map.html (boundary fetch made local); replaces the 4,194-parcel v2 page
- copy SEC_Pipeline/securitization_timeline_map.html -> Securitization_Timeline_Map.html (boundary fetch made local); replaces the 4,194-parcel v2 page
- build Chilton_Tracts_2026.geojson (174 tracts; 170 with canonical values)
- build Chilton_2018_Update.html (canonical 1.23x/0.88x, t-tests, top 20, all 170 tracts, Leaflet choropleth)
- data: OWNERSHIP_CANONICAL_2026-07-22/OPERATOR_ROLLUP_CANONICAL_2026-07-22.csv -> data/OPERATOR_ROLLUP_CANONICAL_2026-07-22.csv
- data: OWNERSHIP_CANONICAL_2026-07-22/Operator_Name_Crosswalk_MASTER_2026-07-22.csv -> data/Operator_Name_Crosswalk_MASTER_2026-07-22.csv
- data: OWNERSHIP_CANONICAL_2026-07-22/Operator_Name_Crosswalk_ADDITIONS_2026-07-22.csv -> data/Operator_Name_Crosswalk_ADDITIONS_2026-07-22.csv
- data: FINAL_OWNERSHIP_DELIVERABLES_2026-07-14/PARENT_SUBSIDIARY_ADDRESS_REGISTRY_2026-07-14.csv -> data/PARENT_SUBSIDIARY_ADDRESS_REGISTRY_2026-07-14.csv
- data: 00_ORGANIZED/01_Who_Owns/Chilton_Update/Burdened_Tract_ReRun_CANONICAL_2026-07-15.csv -> data/Burdened_Tract_ReRun_CANONICAL_2026-07-15.csv
- data: 00_ORGANIZED/01_Who_Owns/Chilton_Update/Tables_CANONICAL_2026-07-15/Table_ConcentrationRatios_CANONICAL.csv -> data/Table_ConcentrationRatios_CANONICAL.csv
- data: 00_ORGANIZED/01_Who_Owns/Chilton_Update/Tables_CANONICAL_2026-07-15/Table6_Burdened_vs_NonBurdened_CANONICAL.csv -> data/Table6_Burdened_vs_NonBurdened_CANONICAL.csv
- data: 00_ORGANIZED/01_Who_Owns/Chilton_Update/Tables_CANONICAL_2026-07-15/Table3_Top20_Tracts_by_EntityRate_CANONICAL.csv -> data/Table3_Top20_Tracts_by_EntityRate_CANONICAL.csv
- data: 00_ORGANIZED/01_Who_Owns/Chilton_Update/Tables_CANONICAL_2026-07-15/Table12_Chilton_TTests_CANONICAL.md -> data/Table12_Chilton_TTests_CANONICAL.md
- data: Who_Owns_2.0/01_Who_Owns/Appendix_A3_owner_group_tiers_2026-10-19.csv -> data/PartI_Appendix_A3_owner_group_tiers_2026-10-19.csv
- data: Who_Owns_2.0/01_Who_Owns/Appendix_A8_operator_tract_ratios_2026-10-19.csv -> data/PartI_Appendix_A8_operator_tract_ratios_2026-10-19.csv
- data: Who_Owns_2.0/01_Who_Owns/Appendix_A9_operator_net_acquisitions_2026-10-19.csv -> data/PartI_Appendix_A9_operator_net_acquisitions_2026-10-19.csv
- data: Who_Owns_2.0/01_Who_Owns/Appendix_A9_operator_gross_acquisitions_2026-10-19.csv -> data/PartI_Appendix_A9_operator_gross_acquisitions_2026-10-19.csv
- data: 00_ORGANIZED/01_Who_Owns/Findings_Tables_Graphics/OO_NOO_Conversion_Shares_2015-2025_2026-07-16.csv -> data/PartI_Appendix_A10_occupancy_conversion_2015-2025.csv
- data: Who_Owns_2.0/02_Who_Rents/Appendix_A_registration_by_operator_2026-10-19.csv -> data/PartII_Appendix_A_registration_by_operator_2026-10-19.csv
- data: Who_Owns_2.0/02_Who_Rents/Appendix_A_registration_by_operator_REGISTRANT_2026-10-19.csv -> data/PartII_Appendix_A_registration_by_operator_REGISTRANT_2026-10-19.csv
- data: Who_Owns_2.0/02_Who_Rents/evictions_operator_plaintiff_detainers_2026-10-19.csv -> data/PartII_evictions_operator_plaintiff_detainers_2026-10-19.csv
- data: Who_Owns_2.0/02_Who_Rents/Registration_delta_new_2026_cases_2026-10-19.csv -> data/PartII_Registration_delta_new_2026_cases_2026-10-19.csv
- data: 00_ORGANIZED/03_Who_Builds/BTR_Share_RECONCILED_2026-07-15.csv -> data/PartIII_BTR_Share_RECONCILED_2026-07-15.csv
- data: Who_Owns_2.0/03_Who_Builds/BTR_parcels_by_tract_2026-10-19.csv -> data/PartIII_BTR_parcels_by_tract_2026-10-19.csv
- data: 00_ORGANIZED/03_Who_Builds/Who_Builds_PublicBuilder_Share_2026-07-03.csv -> data/PartIII_PublicBuilder_Share_2026-07-03.csv
- data: Who_Owns_2.0/04_Who_Landbanks/landbank_live_counts_2026-10-19.json -> data/PartIV_landbank_live_counts_2026-10-19.json
- data: 00_ORGANIZED/04_Who_Finances/SEC_Pipeline/entity_parcel_ownership.csv -> data/PartV_securitized_parcels_1833_entity_parcel_ownership.csv
- data: 00_ORGANIZED/04_Who_Finances/SEC_Pipeline/securitized_parcels_points.geojson -> data/PartV_securitized_parcels_points.geojson
- data: 00_ORGANIZED/04_Who_Finances/SEC_Pipeline/deal_geography_summary.csv -> data/PartV_deal_geography_summary.csv
- data: 00_ORGANIZED/04_Who_Finances/SEC_Pipeline/validation_vs_freddie.csv -> data/PartV_validation_vs_freddie.csv
- data: 00_ORGANIZED/04_Who_Finances/SEC_Pipeline/securitized_by_zip.csv -> data/PartV_securitized_by_zip.csv
- data: 00_ORGANIZED/Lit_Review_Methods/_Audit/PDF_Comparison_Matrix_2026-05-23.csv -> data/Literature_Comparison_Matrix_2026-05-23.csv
- paper: 00_Series_Introduction/Series_Introduction_v4_2026-10-19.docx -> papers/Series_Introduction_v4_2026-10-19.docx
- paper: 01_Who_Owns/Part_I_Who_Owns_Nashville_v2_2026-10-19.docx -> papers/Part_I_Who_Owns_Nashville_v2_2026-10-19.docx
- paper: 02_Who_Rents/Part_II_Who_Rents_Nashville_v7_2026-10-19.docx -> papers/Part_II_Who_Rents_Nashville_v7_2026-10-19.docx
- paper: 03_Who_Builds/Part_III_Who_Builds_Nashville_v2_2026-10-19.docx -> papers/Part_III_Who_Builds_Nashville_v2_2026-10-19.docx
- paper: 04_Who_Landbanks/Part_IV_Who_Landbanks_Nashville_v4_2026-10-19.docx -> papers/Part_IV_Who_Landbanks_Nashville_v4_2026-10-19.docx
- paper: 05_Who_Finances/Part_V_Who_Finances_Nashville_v5_2026-10-19.docx -> papers/Part_V_Who_Finances_Nashville_v5_2026-10-19.docx
- paper: 06_Series_Conclusion/Series_Conclusion_v2_2026-10-19.docx -> papers/Series_Conclusion_v2_2026-10-19.docx
- build index.html
- link check: 0 broken local refs []
