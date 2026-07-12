"""Atlanta-style choropleth — MAP. Replicates the dark-basemap census-tract look
(percent by tract, plasma ramp, manual bins, styled legend box, scale bar) for
Davidson County. Optional contextily dark basemap (needs network); falls back to
a dark background offline."""
import matplotlib; matplotlib.use("Agg")
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.patches import Patch
import geopandas as gpd, numpy as np

ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
gdf = gpd.read_file(os.path.join(ROOT, "Davidson_Institutional_Pct_by_Tract.geojson")).to_crs(32616)  # UTM 16N (m)
col = "pct_institutional"

BINS = [0, 2, 4, 7, 13, 22, 100]
LABELS = ["0 – 2%", "2 – 4%", "4 – 7%", "7 – 13%", "13 – 22%", "22%+"]
base = plt.get_cmap("plasma")
colors = [base(x) for x in np.linspace(0.08, 0.95, len(BINS) - 1)]
cmap = ListedColormap(colors); norm = BoundaryNorm(BINS, cmap.N)

fig, ax = plt.subplots(figsize=(12, 11)); DARK = "#3a3a3a"
fig.patch.set_facecolor(DARK); ax.set_facecolor(DARK)
gdf.plot(column=col, cmap=cmap, norm=norm, linewidth=0.3, edgecolor="white",
         ax=ax, missing_kwds={"color": "#666"})
try:
    import contextily as cx
    cx.add_basemap(ax, crs=gdf.crs, source=cx.providers.CartoDB.DarkMatter)
except Exception:
    pass  # offline: keep the dark background

# styled legend box (bottom-right), like the reference
handles = [Patch(facecolor=c, edgecolor="white", label=l) for c, l in zip(colors, LABELS)]
handles.append(Patch(facecolor="#666", edgecolor="white", label="no data"))
leg = ax.legend(handles=handles, title="Percent by Census Tract", loc="lower right",
                framealpha=0.92, facecolor="#eaeaea", fontsize=11, title_fontsize=12)

# scale bar (5 mi) bottom-left, in projected meters
x0, x1 = ax.get_xlim(); y0, y1 = ax.get_ylim()
bar_m = 5 * 1609.34; bx = x0 + (x1 - x0) * 0.05; by = y0 + (y1 - y0) * 0.05
ax.plot([bx, bx + bar_m], [by, by], color="white", lw=4, solid_capstyle="butt")
ax.text(bx + bar_m / 2, by + (y1 - y0) * 0.012, "5 mi", color="white", ha="center", fontsize=10)

ax.set_title("Davidson County — Institutional Ownership by Census Tract",
             color="white", fontsize=16, pad=12)
ax.axis("off")
plt.tight_layout(); plt.savefig("33_atlanta_style_choropleth.png", dpi=150, facecolor=DARK)
print("wrote 33_atlanta_style_choropleth.png")
