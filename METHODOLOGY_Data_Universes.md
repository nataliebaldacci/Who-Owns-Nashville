# How Who Owns Nashville Counts: Data Universes and Measures

*Methodology. Companion to the [Data Filter Funnel](https://nataliebaldacci.github.io/Who-Owns-Nashville/Data_Filter_Funnel.html), [Historical Owners](https://nataliebaldacci.github.io/Who-Owns-Nashville/Historical_Owners.html), and [Identifying Institutional Players](https://nataliebaldacci.github.io/Who-Owns-Nashville/Methodology_Corporate_Landlords.html). Machine-readable definitions live in `canonical_universes.py`; the full specification lives in `UNIVERSE.md`.*

## The problem

In July 2026 this project's maps reported three different counts for what looked like one quantity. A council-district map counted 20,045 institutional homes. A tract choropleth computed rates against 224,322 residential parcels. The methodology page counted 16,769 entity-owned homes out of 205,933. Each number was internally correct. Each came from a different filter applied at a different time. A reader comparing two maps had no way to know that.

The cause was structural. Every map carried its own data extract, and nothing forced the extracts to share a definition. The fix is also structural: one written specification that names each parcel universe, defines each measure, and requires every map to declare which combination it uses. This page is that specification in narrative form.

## Sources

All data comes from primary government endpoints, and every count can be replayed against them.

1. **Current cadastral.** Metro Nashville parcel layer, one row per parcel with owner, land use, structure type, and assessed value. `https://maps.nashville.gov/arcgis/rest/services/Cadastral/Cadastral_Layers/MapServer/4`. The July 6, 2026 snapshot holds 286,721 parcels.
2. **Ownership history.** Metro ParcelHistory deed record, one row per transfer with the owner name, mailing address, and state at the time of the deed. `https://maps.nashville.gov/arcgis2/rest/services/Parcels/ParcelHistory/MapServer/2`. The record holds 1,641,434 deed events from 2001 forward, including foreclosures.
3. **Parcel service.** Metro's per-parcel SOAP service for assessment history, building characteristics, and sales detail. `https://maps.nashville.gov/ParcelService/Search.asmx?WSDL`. This service is a verification layer, not a universe: we pull it per parcel to cross-check values that the universes produce.

## Three universes

A universe answers one question: which records are we counting? Every dataset in this project belongs to exactly one.

**U1, the framework universe,** holds the existing one- and two-unit homes that the 21st Century Housing Act framework covers. The filter, verbatim from the county query:

```sql
(ducount = 1 OR ducount = 2)
AND ludesc IN ('NULL','SINGLE FAMILY','ZERO LOT LINE','DUPLEX','RESIDENTIAL CONDO')
AND featuretype NOT IN ('Multistory Condo','Multistory Common Area','Open Space')
```

The county query returned 205,933 parcels on July 6, 2026. Two details matter. The county stores unclassified land use as the literal string `'NULL'`, so the filter matches that string rather than a database null. The land-use list must never run without the dwelling-unit condition, because the unclassified category holds 15,807 parcels of every description. U1 feeds the ownership maps, the institutional-rate choropleths, and the tenure, cost-burden, and eviction layers.

**U2, the developable universe,** adds vacant land to U1, because build-to-rent and land-banking analysis must see parcels before homes exist. The vacant test uses a prefix match, `ludesc LIKE 'VACANT%'`, rather than an exact list. The prefix catches Vacant Residential Land, Vacant Rural Land, Vacant Zoned Multi Family, and Vacant Commercial Land, and it also catches the county's misspelling `VACANT RESIENTIAL LAND`, which appears on roughly 60 parcels and which an exact list silently drops. Within U2, a lifecycle field separates built homes from pipeline parcels. U2 feeds the BTR lifecycle, pipeline, and plat maps.

**U3, the deeds universe,** counts transactions rather than parcels: every entity that ever took title, not just the current holder. The corporate test applied to all 1,641,434 deed events yields 199,158 corporate-entity deed events. U3 feeds the acquisition timelines and the historical owner rankings.

## Three measures

A measure answers a second question: how do we split the records? The same three measures apply to any universe, with the same code.

**M1, ownership type,** classifies each recorded owner name as Individual, Entity, Trust, Bank-Lender, or Government. A name is an entity when it carries a business token (LLC, LP, INC, CORP, HOMES, HOLDING, CAPITAL, SFR, BORROWER, and fourteen others) and is not a government body or a trust. Token matching runs against a space-padded, punctuation-stripped copy of the name, and boundary spaces are part of the token. That detail is not cosmetic. An unpadded `HUD` token classifies every Hudson family as a government body, and an unpadded `BANK` token classifies the Banks and Eubanks families as lenders. Both errors occurred and both are now regression tests.

**M2, occupancy and geography,** uses the mailing address on the record. A home is owner-occupied when the owner's mailing ZIP matches the parcel ZIP. An owner is out-of-county when the mailing ZIP falls outside the Davidson County set (37013, 37072, 37076, 37080, 37115, 37138, 37189, 37201 through 37221, and 37228), and out-of-state when the state code is not TN. On U1 these tests mark 42,632 homes as non-owner-occupied and 11,929 as out-of-state owned. On U3 they mark 126,649 deed events as out-of-state.

**M3, operator attribution,** links single-purpose shells back to the operators that control them, through a five-step resolution chain: known-shell name patterns, the Security-for-Sale entity crosswalk, a curated owner-to-operator table built from current holdings, operator name-series rules, and mailing-address clustering verified against the Tennessee Secretary of State registry. The chain is documented in full at [Identifying Institutional Players](https://nataliebaldacci.github.io/Who-Owns-Nashville/Methodology_Corporate_Landlords.html).

One vocabulary rule binds the measures. "Entity-owned" and "corporate" refer to M1, the keyword test. "Institutional" refers to M3 only, owners attributed to a named operator. The two numbers differ by design, and mixing the labels produced the divergent maps this specification replaces.

## The reconciliation

The specification was tested against the project's own baseline file, `Nashville_Framework_Homes_BASELINE_2026-07-07.parquet`, which held 225,471 rows against the county's 205,933. The gap decomposed exactly.

First, 18,071 rows failed the feature-type exclusion, and 18,064 of them were multistory condominiums. The baseline had applied the dwelling-unit condition but not the feature-type exclusion, so high-rise condo units were counted as framework homes. Second, roughly 1,333 rows carried land uses outside the five-value list (407 mobile homes, 319 small office buildings, and a tail of rural combos and dormitories), because the baseline had never applied the land-use list at all. Applying the full filter locally produced 206,067 rows, within 134 of the county count, and the residual is one day of snapshot drift between the July 6 query and the July 7 pull. No parcel appeared twice.

The same test exposed classification errors on both sides. The project's enrichment sent 1,196 community-property trusts to the corporate column and missed 756 truncated living-trust names. The canonical classifier carried the substring bugs described under M1. Both classifiers were corrected against the disagreement list, and twenty real owner names from that list now run as permanent regression tests.

The reconciliation also resolved the legacy number. The 20,045 institutional homes on the older pages was the corporate count on the broad, pre-framework universe (20,873 at the current snapshot). One filter vintage, carried forward by copy, explains every stray count this project ever published.

## The file of record

`Nashville_Framework_Homes_CANONICAL_2026-07-07.parquet` is the U1 file of record: 206,067 homes (156,644 single family, 36,936 residential condo, 7,068 duplex, 5,419 zero lot line), with the corrected M1 classification of every owner (173,132 individual, 16,567 entity, 15,944 trust, 377 government, 47 bank or lender). Every new extract, choropleth, and figure cuts from this file or from a successor derived the same way. Each map states its cut in one line, universe plus measure, so the next divergence announces itself.
