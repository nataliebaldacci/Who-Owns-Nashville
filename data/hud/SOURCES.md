# HUD User API — Davidson County pull (2026-07-11)

All from the HUD User Datasets API, `https://www.huduser.gov/hudapi/public`, Davidson County, TN
(HUD entity id `4703799999`; state `47`, county `037`/`37`; Nashville-Davidson–Murfreesboro–Franklin MSA).
Authenticated with a personal HUD API bearer token (NOT stored in this folder or any script).

## Endpoints pulled
| Dataset | Endpoint | Coverage | Files |
|---|---|---|---|
| Fair Market Rents | `fmr/data/4703799999?year=YYYY` | 2017–2026 | `raw/fmr_Davidson_*.json` (Small Area / ZIP-level where published) |
| Income Limits | `il/data/4703799999?year=YYYY` | 2017–2026 | `raw/il_Davidson_*.json` |
| MTSP Income Limits | `mtspil/data/4703799999?year=YYYY` | 2017–2026 | `raw/mtspil_Davidson_*.json` |
| CHAS (county) | `chas?type=3&stateId=47&entityId=37&year=YYYY-YYYY` | 8 vintages 2011–2015 … 2018–2022 | `raw/chas_Davidson_*.json` |
| USPS crosswalk (tract→ZIP) | `usps?type=7&query=47037` | latest quarter | `raw/usps_tract2zip_Davidson.json` (55 rows) |

## Tidy extracts
- `Davidson_FMR_SmallArea_byZIP_2017-2026.csv` — year, zip_code, eff/1br/2br/3br/4br FMR.
- `Davidson_IncomeLimits_2017-2026.csv` — year, median_income, 4-person 30%/50%/80% limits.

## Notes
- CHAS county requires `entityId=37` (no leading zero) + an explicit `year` range; `entityId=037` returns empty.
- FMR returns ZIP-level Small Area rows for recent years (Nashville MSA `smallarea_status=1`); earlier years may be county-level single rows.
- Raw JSON is the authoritative copy; CSVs are convenience flattenings.
- Token is a credential: kept in an env var only, never written to disk. Rotate at huduser.gov if it was shared anywhere.
