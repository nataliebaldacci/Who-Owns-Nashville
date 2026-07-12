"""Choropleth — MAP (static, geopandas). Davidson tracts shaded by institutional %.
Uses the JCHS orange sequential ramp and quantile classes (mapclassify)."""
import matplotlib; matplotlib.use("Agg")
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import matplotlib.pyplot as plt
import geopandas as gpd
from matplotlib.colors import LinearSegmentedColormap
from styles.won_styles import RAMPS
ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
gdf = gpd.read_file(os.path.join(ROOT, "Davidson_Institutional_Pct_by_Tract.geojson"))
cmap = LinearSegmentedColormap.from_list("jchs_orange", RAMPS["jchs_orange"])
fig, ax = plt.subplots(figsize=(9, 8))
gdf.plot(column="pct_institutional", cmap=cmap, scheme="quantiles", k=5,
         legend=True, linewidth=0.3, edgecolor="#ffffff", ax=ax,
         legend_kwds={"title": "Institutional %", "loc": "lower left", "fontsize": 8},
         missing_kwds={"color": "#dddddd"})
ax.set_title("Institutional Ownership Share by Census Tract — Davidson County",
             fontweight="bold", fontsize=13)
ax.axis("off")
plt.tight_layout(); plt.savefig("18_choropleth.png", dpi=150)
print("wrote 18_choropleth.png")
