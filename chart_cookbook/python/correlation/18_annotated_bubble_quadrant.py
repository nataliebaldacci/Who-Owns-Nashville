"""Annotated quadrant bubble plot (Datawrapper climate-risk style). Block groups
by institutional rate (x) vs poverty rate (y), bubble size = residential parcels,
quadrant reference lines at medians, circled + labeled extreme block groups."""
import matplotlib; matplotlib.use("Agg")
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import matplotlib.pyplot as plt
import geopandas as gpd
ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
bg = gpd.read_file(os.path.join(ROOT, "institutional_by_blockgroup.geojson"))
bg = bg[(bg["rate"].notna()) & (bg["pov"].notna()) & (bg["res"] > 20)].copy()
mx, my = bg["rate"].median(), bg["pov"].median()
colors = ["#1c458c" if (r > mx and p > my) else "#c9d3e0" for r, p in zip(bg["rate"], bg["pov"])]
fig, ax = plt.subplots(figsize=(8, 7))
ax.scatter(bg["rate"], bg["pov"], s=bg["res"]/4, c=colors, marker="s", alpha=0.75,
           edgecolor="white", linewidth=0.4, zorder=2)
ax.axvline(mx, color="gray", ls="--", lw=0.7, alpha=0.5); ax.axhline(my, color="gray", ls="--", lw=0.7, alpha=0.5)
top = bg[(bg["rate"] > mx) & (bg["pov"] > my)].nlargest(5, "res")
for _, r in top.iterrows():
    ax.scatter(r["rate"], r["pov"], s=r["res"]/4, facecolor="none", edgecolor="black", linewidth=1.2, marker="s", zorder=3)
    ax.text(r["rate"], r["pov"]+1.2, str(r["bg"])[-4:], ha="center", size=6)
for sp in ["top","right","bottom","left"]: ax.spines[sp].set_visible(False)
ax.tick_params(length=0)
fig.text(0.09, 0.96, "Where corporate ownership meets economic distress", size=13, weight="bold")
fig.text(0.09, 0.92, "Block groups by institutional rate and poverty; size = residential parcels.\nDark = high on both (upper-right quadrant).", size=9, color="#555")
ax.set_xlabel("Institutional rate (%)"); ax.set_ylabel("Poverty rate (%)")
plt.tight_layout(rect=[0,0,1,0.9]); plt.savefig("18_annotated_bubble_quadrant.png", dpi=150)
print("wrote 18_annotated_bubble_quadrant.png")
