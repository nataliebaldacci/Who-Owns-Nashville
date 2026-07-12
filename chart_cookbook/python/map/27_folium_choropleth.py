"""Folium interactive choropleth — MAP. Davidson tracts shaded by institutional %,
with hover tooltips. Writes 27_folium_choropleth.html (opens in any browser)."""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import geopandas as gpd, folium
ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
gdf = gpd.read_file(os.path.join(ROOT, "Davidson_Institutional_Pct_by_Tract.geojson")).to_crs(4326)
m = folium.Map(location=[36.16, -86.78], zoom_start=10, tiles="CartoDB positron")
folium.Choropleth(
    geo_data=gdf.to_json(), data=gdf, columns=["GEOCODE", "pct_institutional"],
    key_on="feature.properties.GEOCODE", fill_color="OrRd", fill_opacity=0.75,
    line_weight=0.3, legend_name="Institutional ownership (% of residential)",
    nan_fill_color="#dddddd",
).add_to(m)
folium.GeoJson(
    gdf, style_function=lambda x: {"fillOpacity": 0, "color": "transparent"},
    tooltip=folium.GeoJsonTooltip(
        fields=["TRACTCE", "pct_institutional", "inst_parcels", "total_residential"],
        aliases=["Tract:", "Institutional %:", "Inst. parcels:", "Residential:"]),
).add_to(m)
m.save("27_folium_choropleth.html")
print("wrote 27_folium_choropleth.html")
