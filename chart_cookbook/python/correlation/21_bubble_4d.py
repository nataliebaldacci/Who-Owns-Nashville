"""Four-dimensional bubble plot (gapminder style, matplotlib + seaborn). One
point per Davidson block group encoding four variables at once: x = poverty
rate, y = median household income (log scale), bubble SIZE = number of
institutional parcels, bubble COLOR = institutional ownership rate. Includes the
two legends a bubble chart needs — a colorbar for the color variable and a
manual size legend for the size variable. Real data (institutional_by_blockgroup)."""
import matplotlib; matplotlib.use("Agg")
import os
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
bg = gpd.read_file(os.path.join(ROOT, "institutional_by_blockgroup.geojson"))
d = bg[(bg["inc"] > 0) & (bg["inst"].fillna(0) > 0)].copy()

fig, ax = plt.subplots(figsize=(11, 8))
sc = ax.scatter(d["pov"], d["inc"], s=d["inst"].clip(1) * 3, c=d["rate"],
                cmap="plasma", alpha=0.6, edgecolors="white", linewidth=0.8,
                vmin=0, vmax=d["rate"].quantile(0.95))
ax.set_yscale("log")
ax.set_xlabel("Poverty rate (%)"); ax.set_ylabel("Median household income ($, log scale)")
ax.set_title("Four variables at once — Davidson County block groups\n"
             "x poverty · y income · size institutional parcels · color institutional rate",
             fontsize=13, loc="left")
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)

cbar = fig.colorbar(sc, ax=ax, shrink=0.7, pad=0.02)
cbar.set_label("Institutional ownership rate (%)")

# manual size legend (gapminder-style): representative bubble sizes
for val in [10, 50, 150]:
    ax.scatter([], [], s=val * 3, c="grey", alpha=0.5, edgecolors="white",
               linewidth=0.8, label=f"{val} parcels")
ax.legend(scatterpoints=1, frameon=True, labelspacing=1.6, title="Institutional parcels",
          loc="lower right", borderpad=1)

plt.tight_layout()
plt.savefig(os.path.join(os.path.dirname(__file__), "21_bubble_4d.png"), dpi=150)
print("wrote 21_bubble_4d.png  (%d block groups)" % len(d))
