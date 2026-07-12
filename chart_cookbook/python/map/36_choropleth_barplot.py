"""Choropleth + inset bar distribution (Belgium 'Sunset3' style, Koen Van den
Eeckhout / Joseph Barbier). Davidson tracts shaded by institutional %, custom
create_cmap palette, inset bars as the legend, title/subtitle/credit. No region
labels. Reprojected to Web Mercator (EPSG:3857)."""
import matplotlib; matplotlib.use("Agg")
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import matplotlib.pyplot as plt
import geopandas as gpd
from pypalettes import create_cmap

ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
gdf = gpd.read_file(os.path.join(ROOT, "Davidson_Institutional_Pct_by_Tract.geojson")).to_crs(3857)
gdf = gdf[gdf["pct_institutional"].notna()]
col = "pct_institutional"

cmap = create_cmap(
    colors=["#5A1A74", "#661d5c", "#86277A", "#9D2D7A", "#C74370",
            "#FB9A70", "#FDC48C", "#FED69A", "#FCFCBD"][::-1],
    cmap_type="continuous", name="Sunset3")
try:
    from pyfonts import load_google_font
    regular = load_google_font("Roboto"); bold = load_google_font("Roboto", weight="bold")
except Exception:
    regular = bold = None

fig, ax = plt.subplots(figsize=(9, 9), dpi=150); ax.axis("off")
gdf.plot(ax=ax, column=col, cmap=cmap, edgecolor="#e6e6e6", lw=0.3)

bar_ax = ax.inset_axes(bounds=[0.04, 0.10, 0.40, 0.28], zorder=-1)
n, bins, _ = bar_ax.hist(gdf[col], bins=18, alpha=0)
colors = [cmap((b - bins.min()) / (bins.max() - bins.min())) for b in bins]
bar_ax.bar(bins[:-1], n, color=colors, width=(bins[1]-bins[0]))
bar_ax.spines[["top", "left", "right"]].set_visible(False); bar_ax.set_yticks([])
bar_ax.tick_params(axis="x", length=2, labelsize=8); bar_ax.set_xlabel("Institutional %", size=8)

fig.text(0.13, 0.88, "Institutional Ownership in Davidson County", size=14,
         **({"font": bold} if bold else {"weight": "bold"}))
fig.text(0.13, 0.855, "By census tract, share of residential parcels", size=9,
         **({"font": regular} if regular else {}))
fig.text(0.13, 0.12, "Who Owns Nashville · Metro Ownership Parcels", size=6, color="#909090",
         **({"font": regular} if regular else {}))
plt.savefig("36_choropleth_barplot.png", dpi=150, bbox_inches="tight")
print("wrote 36_choropleth_barplot.png")
