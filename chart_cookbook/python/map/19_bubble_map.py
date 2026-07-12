"""Bubble map — MAP (static, geopandas). County outline + one bubble per block
group, sized by institutional-parcel count, colored by rate."""
import matplotlib; matplotlib.use("Agg")
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import matplotlib.pyplot as plt
import geopandas as gpd
from matplotlib.colors import LinearSegmentedColormap
from styles.won_styles import RAMPS
ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
bg = gpd.read_file(os.path.join(ROOT, "institutional_by_blockgroup.geojson"))
try:
    outline = gpd.read_file(os.path.join(ROOT, "Davidson_County_Boundary.geojson"))
except Exception:
    outline = None
cent = bg.copy(); cent["geometry"] = bg.geometry.centroid
cmap = LinearSegmentedColormap.from_list("jchs_orange", RAMPS["jchs_orange"])
fig, ax = plt.subplots(figsize=(9, 8))
if outline is not None:
    outline.plot(ax=ax, color="#eef4fb", edgecolor="#1c458c", linewidth=1)
cent.plot(ax=ax, markersize=cent["inst"].clip(lower=1) * 4, column="rate",
          cmap=cmap, alpha=0.75, edgecolor="white", linewidth=0.3, legend=True,
          legend_kwds={"label": "Institutional rate (%)", "shrink": 0.5})
ax.set_title("Institutional Holdings by Block Group (bubble size = parcel count)",
             fontweight="bold", fontsize=12)
ax.axis("off")
plt.tight_layout(); plt.savefig("19_bubble_map.png", dpi=150)
print("wrote 19_bubble_map.png")
