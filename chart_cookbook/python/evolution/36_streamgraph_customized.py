"""Customized streamgraph — colors, order and smoothing (python-graph-gallery
X-Men "mutant moneyball" style). Demonstrates the full customization workflow on
a streamgraph: (1) color each band by its total via a normalized cm.Reds ramp,
(2) reorder bands by total with np.argsort, (3) smooth with scipy interp1d
(quadratic) and draw with baseline='wiggle'. Real data: corporate SFR
acquisitions per year for the largest owner entities in Davidson County."""
import matplotlib; matplotlib.use("Agg")
import os, json, collections
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
props = [f["properties"] for f in
         json.load(open(os.path.join(ROOT, "Davidson_Active_Corporate_SFR_Detail.geojson")))["features"]]

YEARS = list(range(2013, 2026))
counts = collections.defaultdict(lambda: collections.Counter())
for p in props:
    a, o = str(p.get("acq", ""))[:4], p.get("owner")
    if a.isdigit() and o and 2013 <= int(a) <= 2025:
        counts[o][int(a)] += 1

# top 14 owners by total acquisitions
top = sorted(counts, key=lambda o: -sum(counts[o].values()))[:14]
issues_list = np.array([[counts[o].get(y, 0) for y in YEARS] for o in top], dtype=float)
members = np.array([o.title()[:22] for o in top])

# (1) color by total appearances (normalized cm.Reds)
totals = issues_list.sum(axis=1)
colors = plt.cm.Reds(0.25 + 0.75 * totals / totals.max())

# (2) reorder bands by total
idx = np.argsort(totals)
issues_list, members, colors = issues_list[idx], members[idx], colors[idx]

# (3) smooth with interp1d (quadratic) and draw with a wiggle baseline
xs = np.array(YEARS, dtype=float)
xs_smooth = np.linspace(xs.min(), xs.max(), len(xs) * 10)
smoothed = np.clip([interp1d(xs, row, kind="quadratic")(xs_smooth) for row in issues_list], 0, None)

fig, ax = plt.subplots(figsize=(12, 7))
ax.stackplot(xs_smooth, smoothed, labels=members, colors=colors,
             edgecolor="black", linewidth=0.2, baseline="wiggle")
ax.set_title("Who was buying, and when — Davidson corporate SFR acquisitions\n"
             "streamgraph, bands colored and ordered by total acquisitions, smoothed",
             fontsize=13, loc="left")
ax.set_xlabel("Acquisition year")
ax.set_yticks([])
for s in ["top", "right", "left"]:
    ax.spines[s].set_visible(False)
ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1), fontsize=8, frameon=False,
          title="Owner (by total)")
fig.text(0.09, 0.02, "Source: Who Owns Nashville, Davidson County active corporate SFR detail",
         fontsize=8, color="#5a5a5a")
fig.tight_layout()
plt.savefig(os.path.join(os.path.dirname(__file__), "36_streamgraph_customized.png"),
            dpi=150, bbox_inches="tight")
print("wrote 36_streamgraph_customized.png  (%d owners)" % len(top))
