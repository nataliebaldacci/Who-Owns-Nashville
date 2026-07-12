"""Interactive dark choropleth — MAP. Leaflet/folium version matching the ACS
maps already on the site: CartoDB dark tiles, binned plasma choropleth, and a
hover tooltip per tract. Writes 34_folium_dark_interactive.html."""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import geopandas as gpd, folium, branca.colormap as bcm

ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
gdf = gpd.read_file(os.path.join(ROOT, "Davidson_Institutional_Pct_by_Tract.geojson")).to_crs(4326)
col = "pct_institutional"
BINS = [0, 2, 4, 7, 13, 22, 100]
cmap = bcm.StepColormap(["#4b0c6b", "#812581", "#b5367a", "#e35a63", "#fca636", "#f0f921"],
                        vmin=0, vmax=100, index=BINS, caption="Institutional ownership (% of residential)")

m = folium.Map(location=[36.16, -86.78], zoom_start=10, tiles="CartoDB dark_matter")
folium.GeoJson(
    gdf, name="Institutional % by tract",
    style_function=lambda f: {"fillColor": cmap(f["properties"][col] or 0),
                              "color": "white", "weight": 0.4, "fillOpacity": 0.78},
    highlight_function=lambda f: {"weight": 2, "color": "#00e5ff"},
    tooltip=folium.GeoJsonTooltip(
        fields=["TRACTCE", col, "inst_parcels", "total_residential"],
        aliases=["Tract:", "Institutional %:", "Inst. parcels:", "Residential:"],
        localize=True),
).add_to(m)
cmap.add_to(m); folium.LayerControl().add_to(m)
m.save("34_folium_dark_interactive.html")
print("wrote 34_folium_dark_interactive.html")
