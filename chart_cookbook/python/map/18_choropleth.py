"""
Choropleth map — MAP
Regions shaded by a value. Needs `geopandas` (pip install geopandas).
Inspired by python-graph-gallery.com. This project already ships tract
GeoJSON (e.g. Davidson_Institutional_Pct_by_Tract.geojson) you can load directly.
"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import geopandas as gpd

# Point this at one of the repo's GeoJSON layers:
GEOJSON = "../../../Davidson_Institutional_Pct_by_Tract.geojson"
VALUE_COL = "inst_pct"   # <-- set to the numeric field you want to shade by

gdf = gpd.read_file(GEOJSON)
fig, ax = plt.subplots(figsize=(8, 8))
gdf.plot(column=VALUE_COL, cmap="OrRd", legend=True, linewidth=0.3,
         edgecolor="#dddddd", ax=ax,
         missing_kwds={"color": "#dddddd", "label": "No data"})
ax.set_title("Institutional Ownership Share by Tract", fontweight="bold")
ax.axis("off")
plt.tight_layout()
plt.savefig("18_choropleth.png", dpi=150)
