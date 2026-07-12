"""Choropleth with a custom rectangle legend + arrow annotation (Joseph Barbier
CO2-Europe style). Davidson tracts shaded by institutional %, BrwnYl ramp, a
hand-built swatch legend, centroid labels on the highest tracts, and a drawarrow
arrow calling out a small high-value tract. Optional pyfonts."""
import matplotlib; matplotlib.use("Agg")
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import matplotlib.pyplot as plt, geopandas as gpd
from pypalettes import load_cmap
from drawarrow import fig_arrow
try:
    from highlight_text import ax_text, fig_text
except Exception:
    ax_text = fig_text = None
ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
data = gpd.read_file(os.path.join(ROOT, "Davidson_Institutional_Pct_by_Tract.geojson"))
data = data[data["pct_institutional"].notna()].copy()
cmap = load_cmap("BrwnYl", cmap_type="continuous")
vmax = data["pct_institutional"].quantile(0.97)
fig, ax = plt.subplots(figsize=(10, 10)); fig.set_facecolor("white")
data.plot(ax=ax, column="pct_institutional", cmap=cmap, edgecolor="black", linewidth=0.3, vmax=vmax)
ax.set_axis_off()
# hand-built rectangle legend
ranges = [0, 2, 4, 7, 10, 15, 22]; labels = ["0-2%","2-4%","4-7%","7-10%","10-15%","15%+"]
xmin, xmax = ax.get_xlim(); ymin, ymax = ax.get_ylim()
lx = xmin + (xmax-xmin)*0.02; ly = ymin + (ymax-ymin)*0.30; step = (ymax-ymin)*0.035
w = (xmax-xmin)*0.02; h = (ymax-ymin)*0.028
for i, lab in enumerate(labels):
    v = ((ranges[i]+ranges[i+1])/2)/ranges[-1]
    ax.add_patch(plt.Rectangle((lx, ly - i*step), w, h, color=cmap(v), ec="black", lw=0.6))
    ax.text(lx + w*1.6, ly - i*step + h/2, lab, fontsize=10, va="center")
# centroid labels for the top tracts
proj = data.to_crs(3035); data["cx"] = proj.centroid.to_crs(data.crs).x; data["cy"] = proj.centroid.to_crs(data.crs).y
for _, r in data.nlargest(6, "pct_institutional").iterrows():
    tc = "white" if r["pct_institutional"] > 12 else "black"
    ax.text(r["cx"], r["cy"], f"{r['TRACTCE']}: {r['pct_institutional']:.0f}", fontsize=7, ha="center", va="center", color=tc)
# arrow calling out the single highest tract
top = data.loc[data["pct_institutional"].idxmax()]
fig_arrow(tail_position=(0.30, 0.80), head_position=(0.52, 0.55), radius=0.25,
          width=0.5, head_width=4, head_length=8, color="black")
fig.text(0.30, 0.82, f"Tract {top['TRACTCE']}: {top['pct_institutional']:.0f}% institutional",
         ha="center", fontsize=9, weight="bold")
fig.text(0.5, 0.13, "Institutional Ownership by Census Tract — Davidson County", ha="center", size=20, weight="bold")
fig.text(0.5, 0.10, "Unit: % of residential parcels  ·  Data: Metro Ownership Parcels  ·  Viz: Who Owns Nashville",
         ha="center", size=10, color="#555")
plt.savefig("39_choropleth_custom_legend.png", dpi=150, bbox_inches="tight")
print("wrote 39_choropleth_custom_legend.png")
