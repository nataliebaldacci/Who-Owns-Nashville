"""INSEE 'salary pyramid' style annotated histogram (Joseph Barbier translation).
A horizontal histogram of Davidson home-value ranges with a per-bar color gradient,
title/subtitle/credit, a gold highlight rectangle, and percentage labels."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.patches as patches
import numpy as np, pandas as pd

rng = np.random.default_rng(7)
vals = rng.lognormal(mean=np.log(400), sigma=0.55, size=60000)  # $000s, ~median 400k
edges = list(range(0, 1100, 100)) + [1500, 3000]
labels = [f"${a}-{b}k" for a, b in zip(edges[:-1], edges[1:])]
labels[-1] = f"${edges[-2]}k+"
counts = pd.cut(vals, bins=edges, labels=labels).value_counts().reindex(labels).fillna(0)
pct = 100 * counts / counts.sum()

colors = ['navy','steelblue','steelblue','black','black','darkred','darkred',
          'darkred','red','red','lightcoral','lightsalmon','orange','yellow']
colors = (colors + ['lightyellow'] * len(labels))[:len(labels)]

fig, ax = plt.subplots(figsize=(7, 9))
ax.set_facecolor('whitesmoke'); fig.set_facecolor('whitesmoke')
ax.barh(labels, counts.values, color=colors, zorder=2)
ax.grid(linestyle='-', alpha=0.5, axis='x')
for sp in ['top', 'right', 'bottom']:
    ax.spines[sp].set_visible(False)
ax.tick_params(axis='y', labelsize=11); ax.xaxis.tick_top()

fig.text(0.02, 0.97, "The price pyramid", fontsize=24, fontweight='bold', ha='left')
fig.text(0.02, 0.925, "Distribution of Davidson County home values\nby range (and share of parcels)",
         fontsize=12, color='dimgrey', ha='left')
fig.text(0.02, 0.04, "Illustrative distribution · Who Owns Nashville · Metro Ownership Parcels",
         fontsize=9, color='dimgrey', ha='left')

# gold highlight on the modal (largest) bar
mode_i = int(np.argmax(counts.values))
ax.add_patch(patches.Rectangle((0, mode_i - 0.45), counts.values[mode_i], 0.9,
             linewidth=2, edgecolor='gold', facecolor='none', zorder=3))
for i, p in enumerate(pct.values):
    if p > 0.5:
        ax.text(counts.values[i] + counts.max()*0.01, i, f"{p:.1f}%", va='center', size=9)
plt.tight_layout()
plt.savefig("distribution/28_insee_pyramid.png".split("/")[-1], dpi=150, bbox_inches="tight")
print("wrote 28_insee_pyramid.png")
