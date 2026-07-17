# Parcel GIS Endpoints for Major Corporate Landlord Markets

Reference for pulling parcel and owner data in markets outside Nashville with heavy institutional single family rental presence. Use `pull_tennessee_gis.py` for every endpoint here. It works on any ArcGIS REST service, not just Tennessee. Run `verify_gis_endpoints.py` first to confirm which endpoints are live and which layer carries owner names.

A key pattern: four states publish statewide parcel layers with owner names. One endpoint covers every county in the state. This is far easier than hunting county by county.

## Statewide layers (best starting points)

### Tennessee (already in hand)
Covers all 95 counties including the BTR ring around Nashville (Rutherford, Wilson, Sumner, Williamson, Montgomery).
- Boundaries: https://services1.arcgis.com/YuVBSS7Y1of2Qud1/arcgis/rest/services/Tennessee_Property_Boundaries_Public_Use/FeatureServer/0
- Assessment with OWNER, APPRAISAL, SALEDATE, mailing address: https://maps.cot.tn.gov/server3/rest/services/IMPACT/Labels_Reappraisal/FeatureServer/13

### Florida (Tampa, Jacksonville, Orlando, Lakeland)
FDOR statewide cadastral. About 10.8 million parcels joined to the property tax roll. Owner field is OWN_NAME. Covers Hillsborough, Pasco, Polk, Duval, Orange, Osceola and every other county.
- https://services9.arcgis.com/Gh9awoU677aKree0/arcgis/rest/services/Florida_Statewide_Cadastral/FeatureServer/0

### North Carolina (Charlotte, Raleigh, Winston Salem)
NC OneMap statewide parcels. All 100 counties with ownership, acreage, and assessed value. Covers Mecklenburg, Wake, Forsyth, Guilford, Cabarrus, Union.
- https://services.nconemap.gov/secure/rest/services/NC1Map_Parcels/FeatureServer
- County fallback for Charlotte: https://gis.charlottenc.gov/arcgis/rest/services/CountyData/Parcels/MapServer

### Texas (Dallas, Fort Worth, Houston, San Antonio)
TxGIO StratMap statewide land parcels with owner, land use, and value. Refresh cadence varies by county.
- https://feature.geographic.texas.gov/arcgis/rest/services/Parcels/stratmap23_land_parcels_48/MapServer

## County level markets

### Memphis (Shelby County TN)
Not in the state IMPACT layer. Shelby runs its own system.
- Root: https://gis.shelbycountytn.gov/arcgis/rest/services
- Assessor parcels: https://gis.shelbycountytn.gov/public/rest/services/BaseMap/Assessor/MapServer

### Knoxville (Knox County TN)
Also self assessed. KGIS is the joint city county system.
- Root: https://www.kgis.org/arcgis/rest/services

### Atlanta (Fulton, Gwinnett, Cobb, DeKalb, Clayton, Henry GA)
Georgia has no open statewide parcel service. Each county publishes separately.
- Fulton root: https://gismaps.fultoncountyga.gov/arcgispub2/rest/services
- Fulton open data hub: https://gisdata.fultoncountyga.gov
- DeKalb root: https://dcgis.dekalbcountyga.gov/hosted/rest/services
- Cobb hub: https://geo-cobbcountyga.hub.arcgis.com
- Gwinnett hub: https://gcgis-gwinnettcountyga.hub.arcgis.com
- Atlanta Regional Commission (regional layers): https://arcgis.atlantaregional.com/arcgis/rest/services
- Clayton and Henry publish through vendor portals. Verify with the checker script.

### Phoenix (Maricopa County AZ)
Assessor query service with 57 fields including OWNER_NAME, mailing address, DEED_DATE, SALE_DATE, SALE_PRICE.
- Parcels layer: https://gis.mcassessor.maricopa.gov/arcgis/rest/services/MaricopaDynamicQueryService/MapServer/3
- Root: https://gis.mcassessor.maricopa.gov/arcgis/rest/services

### Las Vegas (Clark County NV)
- Roots: https://maps.clarkcountynv.gov/arcgis/rest/services and https://gisgate.co.clark.nv.us/arcgis/rest/services
- Nevada statewide fallback: https://arcgis.water.nv.gov/arcgis/rest/services/BaseLayers/County_Parcels_in_Nevada/MapServer

### Indianapolis (Marion County IN)
Candidate root, unverified: https://xmaps.indy.gov/arcgis/rest/services

## Workflow

Verify first. Run the checker locally. It probes every endpoint above, finds parcel layers, detects owner fields, and writes a CSV inventory.

```
~/Desktop/Master_Data/Scripts/venv/bin/python ~/Desktop/Master_Data/Scripts/verify_gis_endpoints.py
```

Then pull with owner filters instead of whole counties. The pull script accepts any where clause, so a targeted pull of operator owned parcels is small and fast. Example for Florida statewide:

```
~/Desktop/Master_Data/Scripts/venv/bin/python ~/Desktop/Master_Data/Scripts/pull_tennessee_gis.py pull \
  "https://services9.arcgis.com/Gh9awoU677aKree0/arcgis/rest/services/Florida_Statewide_Cadastral/FeatureServer/0" \
  --name FL_Progress_Residential \
  --where "OWN_NAME LIKE 'PROGRESS RESID%'" \
  --outdir ~/Desktop/Master_Data/SFR_Markets
```

Confirm the owner field name from the checker output before writing the where clause. Field names differ by service: OWNER, OWN_NAME, OWNER_NAME, OWNERNAME, OWNNAME1 all appear in the wild. Operators also hold title under many entity names, so search with several LIKE patterns per operator and check both owner and mailing address fields.
