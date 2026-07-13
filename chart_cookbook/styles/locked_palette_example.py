"""Example: the locked palette applied to real figures via op_color() and ramp().
Left = operator parcels bar chart using the locked per-operator colors
(Progress red, American blue, ...). Right = institutional-rate choropleth using
the locked 'institutional' ramp (SunsetDark_7)."""
import matplotlib; matplotlib.use("Agg")
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import matplotlib.pyplot as plt
import geopandas as gpd
from styles.locked_palette import op_color, ramp, NAVY

ROOT = os.path.join(os.path.dirname(__file__), "..", "..")
rows = json.load(open(os.path.join(ROOT, "owner_leaderboard.json")))["rows"][:8]
names = [r["nm"] for r in rows]
parcels = [r["n"] for r in rows]
colors = [op_color(n) for n in names]          # <-- locked operator colors

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6.5), gridspec_kw={"width_ratios": [1, 1.1]})

# left: operator bar chart with locked colors
y = range(len(names))[::-1]
ax1.barh(list(y), parcels, color=colors, edgecolor="white")
for yi, n, p in zip(y, names, parcels):
    ax1.text(p + 12, yi, f"{p:,}", va="center", fontsize=10, color="#333")
ax1.set_yticks(list(y)); ax1.set_yticklabels(names, fontsize=10)
ax1.set_title("Operators — locked colors (op_color)", loc="left", fontweight="bold", color=NAVY)
ax1.set_xlabel("parcels held")
for s in ["top", "right"]:
    ax1.spines[s].set_visible(False)

# right: institutional-rate choropleth with the locked SunsetDark ramp
g = gpd.read_file(os.path.join(ROOT, "Davidson_Institutional_Pct_by_Tract.geojson")).to_crs(3857)
g = g[g["pct_institutional"].notna()]
g.plot(column="pct_institutional", cmap=ramp("institutional"), scheme="quantiles", k=6,
       linewidth=0.15, edgecolor="white", legend=True, ax=ax2,
       legend_kwds={"loc": "lower left", "fontsize": 8, "title": "Institutional %"})
ax2.set_title("Institutional rate by tract — locked ramp (SunsetDark_7)",
              loc="left", fontweight="bold", color=NAVY)
ax2.axis("off")

fig.suptitle("Who Owns Nashville — locked palette in use", fontsize=16, fontweight="bold",
             x=0.02, ha="left")
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig(os.path.join(os.path.dirname(__file__), "..", "figures", "locked_palette_example.png"),
            dpi=140, bbox_inches="tight")
print("wrote figures/locked_palette_example.png")
print("colors used:", dict(zip(names, colors)))
