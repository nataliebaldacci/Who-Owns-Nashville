# Tennessee Statewide GIS Sources

Reference for pulling statewide parcel and assessment data. The downloader script is `pull_tennessee_gis.py` in this repo.

## Sources

### 1. Comptroller IMPACT services folder

Full URL: https://maps.cot.tn.gov/server3/rest/services/IMPACT

This is the Tennessee Comptroller of the Treasury's ArcGIS Server folder for the IMPACT property assessment system. It holds multiple services. Each service holds one or more layers.

### 2. IMPACT Parcel Layer Themes

Full URL: https://maps.cot.tn.gov/server3/rest/services/IMPACT/Parcel_Layer_Themes/FeatureServer/0

This is one layer inside the IMPACT folder. It carries statewide parcels with assessment attributes used for thematic display. Pulling the whole IMPACT folder with the script also captures this layer.

### 3. Tennessee Property Boundaries Public Use

Full URL: https://services1.arcgis.com/YuVBSS7Y1of2Qud1/arcgis/rest/services/Tennessee_Property_Boundaries_Public_Use/FeatureServer/0

This is the statewide parcel boundary fabric hosted on ArcGIS Online. It covers all 95 counties and holds roughly three million parcel polygons. A full statewide pull with geometry produces a multi gigabyte file. Pull one county at a time or pull attributes only unless the full fabric is needed.

## How to pull

Inspect first. The inspect command prints every service, layer, field name, feature count, and record limit. Build where clauses from the field names it prints. Do not guess field names.

```
python3 pull_tennessee_gis.py inspect "https://maps.cot.tn.gov/server3/rest/services/IMPACT"
python3 pull_tennessee_gis.py inspect "https://services1.arcgis.com/YuVBSS7Y1of2Qud1/arcgis/rest/services/Tennessee_Property_Boundaries_Public_Use/FeatureServer/0"
```

Pull one layer for Davidson County. Replace the field name in the where clause with the real county field printed by inspect.

```
python3 pull_tennessee_gis.py pull \
  "https://services1.arcgis.com/YuVBSS7Y1of2Qud1/arcgis/rest/services/Tennessee_Property_Boundaries_Public_Use/FeatureServer/0" \
  --name TN_Parcels_Davidson --where "COUNTY = 'DAVIDSON'"
```

Pull statewide attributes without geometry. This is much smaller and works well for ownership analysis in a spreadsheet or database.

```
python3 pull_tennessee_gis.py pull \
  "https://services1.arcgis.com/YuVBSS7Y1of2Qud1/arcgis/rest/services/Tennessee_Property_Boundaries_Public_Use/FeatureServer/0" \
  --name TN_Parcels_Statewide_attrs --no-geometry
```

Pull everything in the IMPACT folder.

```
python3 pull_tennessee_gis.py pull-folder "https://maps.cot.tn.gov/server3/rest/services/IMPACT"
```

## Output

Each pull writes three files to the output folder. Default output folder is `~/Desktop/Master_Data/TN_Statewide/`. Override with `--outdir`.

1. `.ndjson` is the raw download stream. One feature per line.
2. `.geojson` is the assembled FeatureCollection in WGS84 for mapping.
3. `.csv` is the attribute table for Excel and analysis.

Downloads resume automatically. If a pull stops partway, run the same command again and it continues from the last saved feature.

## Network note for Claude Code cloud sessions

The cloud session network policy currently blocks `maps.cot.tn.gov` and `services1.arcgis.com`. Two ways to run the pull:

1. Run the script locally on your own machine. It needs only Python 3 and the `requests` package.
2. Add both domains to the allowed domains list in the Claude Code environment settings at claude.ai/code, then start a new session and ask Claude to run the pull there. A full statewide geometry pull may exceed the session disk allowance, so prefer county subsets or attribute only pulls in cloud sessions.
