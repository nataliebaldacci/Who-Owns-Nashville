"""
Bubble map — MAP
Point markers sized by a value over a basemap outline. Needs `geopandas`.
Inspired by python-graph-gallery.com.
"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd

# County outline for context (repo ships Davidson_County_Boundary.geojson)
BOUNDARY = "../../../Davidson_County_Boundary.geojson"

# sample operator points (lon, lat, holdings)
pts = pd.DataFrame({
    "operator": ["Progress", "AMH", "Amherst"],
    "lon": [-86.72, -86.78, -86.68],
    "lat": [36.10, 36.16, 36.05],
    "parcels": [1215, 1182, 699],
})
gpts = gpd.GeoDataFrame(pts, geometry=gpd.points_from_xy(pts.lon, pts.lat), crs="EPSG:4326")

fig, ax = plt.subplots(figsize=(8, 8))
try:
    gpd.read_file(BOUNDARY).plot(ax=ax, color="#eef4fb", edgecolor="#1c458c", linewidth=1)
except Exception:
    pass
gpts.plot(ax=ax, markersize=pts["parcels"] / 3, color="#f0af1e", edgecolor="#1c458c", alpha=0.8)
ax.set_title("Operator Holdings (bubble size = parcels)", fontweight="bold")
ax.axis("off")
plt.tight_layout()
plt.savefig("19_bubble_map.png", dpi=150)
