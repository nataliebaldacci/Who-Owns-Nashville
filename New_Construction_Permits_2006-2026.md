# New Residential Construction in Davidson County, 2006–2026

**Prepared:** June 15, 2026
**Universe:** Completed new-construction residential permits (`Case_Type = 'CARN'`, `STATUS_CODE = 'Done'`, sub-types CAA01R301, CAA03R301, CAA02R302), grouped by the year the permit was accepted and by housing type. Construction value (`CONSTVAL`) is the cost to build declared on the permit, not market value.

## What the record shows

New single-family construction collapsed during the Great Recession, recovered after 2012, and ran at more than 3,000 completed homes a year from 2016 through 2022. The permit count peaks in 2017 at 3,739 single-family homes, with 2016, 2019, 2021, and 2022 all close behind. Counting all three housing types, total new units peak in 2022 at 4,815. Declared construction value roughly doubled across the period, from about $151,000 per single-family home in 2006 to about $320,000 in 2024 and 2025, and the average new house grew from roughly 2,600 square feet to over 3,000 after 2020.

Two structural shifts stand out. Townhome and multifamily construction is volatile and swings with the cycle, surging to 1,087 units in 2015 and 1,210 in 2022 but nearly vanishing in 2017 and 2018. Duplex construction was negligible for fifteen years, then jumped from 30 units in 2019 to 121 in 2020 and 128 in 2021, the signature of Nashville's recent two-unit infill activity, before tapering.

| Year | Single Family | Townhome/MF | Duplex | Total units | SF avg build cost |
|---:|---:|---:|---:|---:|---:|
| 2006 | 502 | 340 | 4 | 850 | $151,192 |
| 2007 | 1,329 | 568 | 24 | 1,945 | $166,237 |
| 2008 | 716 | 575 | 14 | 1,319 | $207,702 |
| 2009 | 601 | 308 | 8 | 925 | $206,687 |
| 2010 | 587 | 273 | 3 | 866 | $209,147 |
| 2011 | 571 | 334 | 14 | 933 | $225,452 |
| 2012 | 814 | 337 | 21 | 1,193 | $235,747 |
| 2013 | 1,244 | 399 | 15 | 1,673 | $232,785 |
| 2014 | 1,927 | 652 | 26 | 2,631 | $232,615 |
| 2015 | 2,733 | 1,087 | 11 | 3,842 | $235,830 |
| 2016 | 3,666 | 405 | 25 | 4,121 | $245,045 |
| 2017 | 3,739 | 162 | 8 | 3,917 | $245,621 |
| 2018 | 3,282 | 191 | 5 | 3,483 | $252,196 |
| 2019 | 3,365 | 575 | 30 | 4,000 | $257,295 |
| 2020 | 2,960 | 694 | 121 | 3,896 | $295,716 |
| 2021 | 3,390 | 788 | 128 | 4,434 | $315,346 |
| 2022 | 3,449 | 1,210 | 78 | 4,815 | $317,788 |
| 2023 | 2,129 | 904 | 46 | 3,125 | $321,371 |
| 2024 | 1,925 | 290 | 47 | 2,309 | $320,586 |
| 2025 | 1,113 | 263 | 15 | 1,406 | $320,498 |
| 2026* | 25 | 4 | 0 | 29 | $318,502 |

\*2026 is a partial year.

## The decline after 2022 is partly an artifact

The filter counts only permits marked `Done`, so a permit pulled recently but not yet finished is excluded. That makes the apparent drop from 2022 to 2025 overstate the real slowdown, because many 2023–2025 homes are still under construction and will move into the `Done` count later. Read the recent decline as a floor that will rise, not a final figure, and treat 2026 as essentially empty.

## Caveats

`CONSTVAL` is the builder's declared construction cost on the permit application, useful as a build-cost trend but not a sale price or market value. Total units sums single-family and townhome permits (one unit each) with duplex permits (two units each). The sub-type codes restrict the set to detached single-family, townhome/multifamily attached, and duplex new construction; they exclude additions, renovations, and accessory dwelling units. The completion-status filter means recent-year counts are provisional.

## Source and replay URLs

Metropolitan Nashville and Davidson County, Permit History (ArcGIS ParcelHistory MapServer Layer 4), filtered to `STATUS_CODE = 'Done' AND Case_Type = 'CARN' AND Sub_type IN ('CAA01R301','CAA03R301','CAA02R302')`, grouped by year accepted and sub-type (last accessed June 15, 2026).

Layer endpoint:

```
https://maps.nashville.gov/arcgis2/rest/services/Parcels/ParcelHistory/MapServer/4
```

Full query, the exact call behind this table (HTML):

```
https://maps.nashville.gov/arcgis2/rest/services/Parcels/ParcelHistory/MapServer/4/query?where=STATUS_CODE+%3D+%27Done%27+and+Case_Type+%3D+%27CARN%27+and+Sub_type+IN+%28%27CAA01R301%27%2C%27CAA03R301%27%2C%27CAA02R302%27%29&outFields=&returnGeometry=false&orderByFields=EXTRACT%28YEAR+FROM+Date_Accepted%29+asc&groupByFieldsForStatistics=EXTRACT%28YEAR+FROM+Date_Accepted%29%2CSUB_TYPE_DESC%2CSTATUS_CODE&outStatistics=%5B%7B%22statisticType%22%3A%22count%22%2C%22onStatisticField%22%3A%22CA_OBJECT_ID%22%2C%22outStatisticFieldName%22%3A%22Permit_Count%22%7D%2C%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22UNITS%22%2C%22outStatisticFieldName%22%3A%22Total_Units%22%7D%2C%7B%22statisticType%22%3A%22avg%22%2C%22onStatisticField%22%3A%22CONSTVAL%22%2C%22outStatisticFieldName%22%3A%22Avg_ConstVal%22%7D%2C%7B%22statisticType%22%3A%22avg%22%2C%22onStatisticField%22%3A%22BLDG_SQ_FT%22%2C%22outStatisticFieldName%22%3A%22Avg_Bldg_SqFt%22%7D%5D&f=html
```

Same query as JSON (swap the final `f=html` for `f=json`):

```
https://maps.nashville.gov/arcgis2/rest/services/Parcels/ParcelHistory/MapServer/4/query?where=STATUS_CODE+%3D+%27Done%27+and+Case_Type+%3D+%27CARN%27+and+Sub_type+IN+%28%27CAA01R301%27%2C%27CAA03R301%27%2C%27CAA02R302%27%29&outFields=&returnGeometry=false&orderByFields=EXTRACT%28YEAR+FROM+Date_Accepted%29+asc&groupByFieldsForStatistics=EXTRACT%28YEAR+FROM+Date_Accepted%29%2CSUB_TYPE_DESC%2CSTATUS_CODE&outStatistics=%5B%7B%22statisticType%22%3A%22count%22%2C%22onStatisticField%22%3A%22CA_OBJECT_ID%22%2C%22outStatisticFieldName%22%3A%22Permit_Count%22%7D%2C%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22UNITS%22%2C%22outStatisticFieldName%22%3A%22Total_Units%22%7D%2C%7B%22statisticType%22%3A%22avg%22%2C%22onStatisticField%22%3A%22CONSTVAL%22%2C%22outStatisticFieldName%22%3A%22Avg_ConstVal%22%7D%2C%7B%22statisticType%22%3A%22avg%22%2C%22onStatisticField%22%3A%22BLDG_SQ_FT%22%2C%22outStatisticFieldName%22%3A%22Avg_Bldg_SqFt%22%7D%5D&f=json
```

Sub-type codes: `CAA01R301` = Single Family Residence, `CAA03R301` = Multifamily/Townhome, `CAA02R302` = Duplex. To widen the window, drop the `STATUS_CODE = 'Done'` clause from the `where` parameter to include permits still in progress.
