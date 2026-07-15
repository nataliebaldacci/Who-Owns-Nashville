# Boundary / reference layer catalog

Saved sources for Davidson County and Tennessee reference geography, ready to
load on any map page via `won_boundary_layers.js` (lazy overlay toggles) or to
query directly. Every URL is the ArcGIS REST layer endpoint; append
`/query?where=1%3D1&outFields=*&f=geojson` to pull GeoJSON.

## Davidson County

| Layer | Endpoint |
|---|---|
| Subdivisions | https://services2.arcgis.com/HdTo6HJqh92wn4D8/ArcGIS/rest/services/Subdivision_Boundaries/FeatureServer/0 |
| Cadastral layers (live parcels; layer 4 = current) | https://maps.nashville.gov/arcgis/rest/services/Cadastral/Cadastral_Layers/MapServer |
| ZIP codes | https://maps.nashville.gov/arcgis/rest/services/Boundaries/Boundaries/MapServer/0 |
| Community planning areas | https://maps.nashville.gov/arcgis/rest/services/Boundaries/Boundaries/MapServer/1 |
| Council districts (2022, with demographics) | https://services2.arcgis.com/HdTo6HJqh92wn4D8/ArcGIS/rest/services/2022_CouncilDistricts_with_Demographics/FeatureServer/0 |
| Council district demographic profiles | https://services2.arcgis.com/HdTo6HJqh92wn4D8/ArcGIS/rest/services/Council_District_Demographic_Profiles_Public_view/FeatureServer/0 |
| Census areas service (all levels) | https://maps.nashville.gov/arcgis/rest/services/Census/CensusAreas/FeatureServer |
| Census blocks | https://maps.nashville.gov/arcgis/rest/services/Census/CensusAreas/FeatureServer/0 |
| Census block groups | https://maps.nashville.gov/arcgis/rest/services/Census/CensusAreas/FeatureServer/1 |
| Census tracts | https://maps.nashville.gov/arcgis/rest/services/Census/CensusAreas/FeatureServer/2 |
| Community name points | https://services2.arcgis.com/HdTo6HJqh92wn4D8/ArcGIS/rest/services/Davidson_County_Communities_view/FeatureServer/0 |
| County boundary buffer | https://services2.arcgis.com/HdTo6HJqh92wn4D8/ArcGIS/rest/services/DavidsonCountyBoundaryBuffer/FeatureServer/0 |
| County boundary | https://services2.arcgis.com/HdTo6HJqh92wn4D8/ArcGIS/rest/services/Davidson_County_Boundary_1/FeatureServer/0 |
| County buffer, light grey | https://services2.arcgis.com/HdTo6HJqh92wn4D8/ArcGIS/rest/services/Davidson_County_Buffer_Light_Grey/FeatureServer |

## Tennessee / statewide

| Layer | Endpoint |
|---|---|
| Statewide IMPACT services directory | https://maps.cot.tn.gov/server3/rest/services/IMPACT |
| All TN county boundaries | https://services1.arcgis.com/kILp9lqGUeOhnDbI/ArcGIS/rest/services/TN_County_Layer/FeatureServer/0 |
| TN state boundary | https://services4.arcgis.com/QdHwhlbx61LR3TWb/ArcGIS/rest/services/TN_Boundary/FeatureServer/0 |

## Basemap

| Layer | Endpoint |
|---|---|
| Nashville Basemap Muted (cached tiles) | https://maps.nashville.gov/arcgis/rest/services/Basemaps/NashvilleBasemapMuted/MapServer |

## Usage

```html
<script src="won_boundary_layers.js"></script>
<script>
  var ctl = L.control.layers(BASES, null, {position:'topright'}).addTo(map);
  WON_LAYERS.attach(map, ctl);          // adds every catalog layer as an overlay toggle
  // or fetch one directly:
  WON_LAYERS.load('tracts').then(function(gj){ /* GeoJSON FeatureCollection */ });
</script>
```

Layers download from the source service only when first toggled on, and page
past the 2,000-record ArcGIS cap automatically. Census blocks and subdivisions
are large; expect a delay on first toggle.
