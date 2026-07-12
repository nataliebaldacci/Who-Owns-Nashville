"""Choropleth + inset histogram (Joseph Barbier / Python Graph Gallery style).
Davidson tracts shaded by institutional %, with an inset histogram that doubles
as the legend (bars colored by the same continuous cmap). pypalettes 'enara'
ramp; optional pyfonts Google font (falls back to default offline)."""
import matplotlib; matplotlib.use("Agg")
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import matplotlib.pyplot as plt
import geopandas as gpd
from pypalettes import load_cmap

ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
gdf = gpd.read_file(os.path.join(ROOT, "Davidson_Institutional_Pct_by_Tract.geojson"))
gdf = gdf[gdf["pct_institutional"].notna()]
col = "pct_institutional"

try:
    cmap = load_cmap("Enara", cmap_type="continuous", reverse=True)
except Exception:
    cmap = plt.get_cmap("magma_r")
try:
    from pyfonts import load_google_font
    font_body = load_google_font("Ubuntu"); font_title = load_google_font("Roboto Slab")
except Exception:
    font_body = font_title = None

edge = "white"
fig, ax = plt.subplots(figsize=(9, 9), dpi=150)
gdf.plot(ax=ax, column=col, cmap=cmap, edgecolor=edge, linewidth=0.2)
ax.axis("off")

# inset histogram (bottom-left) that acts as the legend
bar_ax = ax.inset_axes(bounds=[0.02, -0.02, 0.42, 0.28], zorder=-1)
n, bins, _ = bar_ax.hist(gdf[col], bins=15, alpha=0)
colors = [cmap((b - bins.min()) / (bins.max() - bins.min())) for b in bins]
bar_ax.bar(bins[:-1], n, color=colors, width=(bins[1]-bins[0]), edgecolor=edge, linewidth=0.4)
bar_ax.spines[["top", "left", "right"]].set_visible(False)
bar_ax.set_yticks([])
bar_ax.tick_params(axis="x", length=0, pad=4, labelsize=8)
bar_ax.set_xlabel("Institutional %", fontsize=8)

# label the highest-institutional tracts
top = gdf.nlargest(3, col)
for _, r in top.iterrows():
    c = r.geometry.representative_point()
    ax.text(c.x, c.y, f"{r['TRACTCE']}\n{r[col]:.0f}%", fontsize=6, ha="center", va="center",
            color="white", **({"font": font_body} if font_body else {}))

fig.text(0.5, 0.92, "Institutional Ownership by Census Tract — Davidson County",
         ha="center", size=18, **({"font": font_title} if font_title else {"weight": "bold"}))
fig.text(0.9, 0.06, "Who Owns Nashville · Metro Ownership Parcels", ha="right", size=7, style="italic")
plt.savefig("35_choropleth_histogram.png", dpi=150, bbox_inches="tight")
print("wrote 35_choropleth_histogram.png")
