"""Choropleth by ZIP — MAP. Spatial-joins corporate-owned parcels to ZIP codes
and shades each ZIP by the count. Shows how to aggregate any point layer to any
boundary via styles.boundaries.aggregate_points()."""
import matplotlib; matplotlib.use("Agg")
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from styles.boundaries import aggregate_points, BOUNDARIES
from styles.won_styles import RAMPS
gdf = aggregate_points("Davidson_Corporate_Ownership_CLEAN.geojson", "zip", how="count")
cmap = LinearSegmentedColormap.from_list("jchs_blue", RAMPS["jchs_blue"])
fig, ax = plt.subplots(figsize=(9, 8))
gdf.plot(column="metric", cmap=cmap, scheme="quantiles", k=5, legend=True,
         linewidth=0.4, edgecolor="white", ax=ax,
         legend_kwds={"title": "Corporate parcels", "loc": "lower left", "fontsize": 8})
lab = BOUNDARIES["zip"][2]
for _, r in gdf.iterrows():
    if r["metric"] > gdf["metric"].quantile(0.8):
        c = r.geometry.representative_point()
        ax.annotate(str(r[lab]), (c.x, c.y), fontsize=6, ha="center", color="#16357a")
ax.set_title("Corporate-Owned Parcels by ZIP Code — Davidson County",
             fontweight="bold", fontsize=13); ax.axis("off")
plt.tight_layout(); plt.savefig("31_choropleth_by_zip.png", dpi=150)
print("wrote 31_choropleth_by_zip.png")
