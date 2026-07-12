"""Dumbbell / lollipop with colormap segments + custom legend (Cedric Scherer
Mario Kart style). Per operator: first-acquisition median value (grey dot) to
latest median value (blue dot); segment colored by the value change (RedOr)."""
import matplotlib; matplotlib.use("Agg")
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import numpy as np, matplotlib.pyplot as plt, matplotlib.colors as mc
from matplotlib.cm import ScalarMappable
from matplotlib.lines import Line2D
from palettable import cartocolors
ops = ["Progress","AMH","Amherst","Regent","Normandy","Tricon","Starwood","FirstKey"]
rng = np.random.default_rng(4)
first = rng.uniform(180, 360, len(ops))           # first-record value ($000s)
latest = first + rng.uniform(40, 180, len(ops))   # latest value (higher)
years = rng.integers(2018, 2025, len(ops))
order = np.argsort(latest)
ops=[ops[i] for i in order]; first=first[order]; latest=latest[order]; years=years[order]
cmap_o = cartocolors.sequential.RedOr_5.mpl_colormap
cmap_b = mc.LinearSegmentedColormap.from_list("blue", ["#b4d1d2", "#242c3c"], N=256)
norm_d = mc.Normalize(0, 200); norm_y = mc.Normalize(years.min(), years.max())
fig, ax = plt.subplots(figsize=(11, 7))
for sp in ax.spines.values(): sp.set_visible(False)
for i, op in enumerate(ops):
    ax.hlines(i, first[i], latest[i], color=cmap_o(norm_d(latest[i]-first[i])), lw=6, zorder=1)
    ax.scatter(first[i], i, s=170, color="#a6a6a6", zorder=2)
    ax.scatter(latest[i], i, s=150, color=cmap_b(norm_y(years[i])), zorder=3)
    ax.text(first[i]-8, i, op, ha="right", va="center", size=12)
ax.set_yticks([]); ax.set_xlim(120, 560)
ax.set_title("Operator portfolio value: first vs latest acquisition", weight="bold", size=14, loc="left")
fig.colorbar(ScalarMappable(norm=norm_d, cmap=cmap_o), ax=ax, shrink=0.4,
             label="Value change ($000s)", location="bottom", pad=0.08)
handles=[Line2D([0],[0],marker="o",lw=0,markersize=9,color=cmap_b(norm_y(y)),label=str(y)) for y in sorted(set(years))]
ax.legend(handles=handles, title="Year of latest", loc="lower right", frameon=False, fontsize=9)
plt.tight_layout(); plt.savefig("05_dumbbell_lollipop.png", dpi=150)
print("wrote 05_dumbbell_lollipop.png")
