"""Small multiples for a line chart (python-graph-gallery anti-spaghetti style).
A 3x3 grid, one panel per owner, each panel drawing every owner's acquisition
curve in faint grey with that panel's owner highlighted in color. Real data:
corporate SFR acquisitions per year for the nine largest owner entities in
Davidson County. Shared axes make the panels directly comparable."""
import matplotlib; matplotlib.use("Agg")
import os, json, collections
import numpy as np
import matplotlib.pyplot as plt

ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
props = [f["properties"] for f in
         json.load(open(os.path.join(ROOT, "Davidson_Active_Corporate_SFR_Detail.geojson")))["features"]]

YEARS = list(range(2012, 2027))
counts = collections.defaultdict(lambda: collections.Counter())
for p in props:
    a = str(p.get("acq", ""))[:4]
    o = p.get("owner")
    if a.isdigit() and o and 2012 <= int(a) <= 2026:
        counts[o][int(a)] += 1

top9 = [o for o, _ in sorted(counts.items(), key=lambda kv: -sum(kv[1].values()))[:9]]
def series(o): return [counts[o].get(y, 0) for y in YEARS]

palette = plt.get_cmap("Set1")
fig, axes = plt.subplots(3, 3, figsize=(13, 12), sharex=True, sharey=True)
axes = axes.flatten()
ymax = max(max(series(o)) for o in top9) * 1.1

for num, owner in enumerate(top9):
    ax = axes[num]
    for other in top9:                      # every owner in faint grey
        ax.plot(YEARS, series(other), color="grey", lw=0.6, alpha=0.3)
    ax.plot(YEARS, series(owner), color=palette(num), lw=2.4, alpha=0.95)
    ax.set_xlim(2012, 2026); ax.set_ylim(0, ymax)
    if num < 6: ax.tick_params(labelbottom=False)
    if num not in [0, 3, 6]: ax.tick_params(labelleft=False)
    label = owner.title()[:26] + ("…" if len(owner) > 26 else "")
    ax.set_title(label, loc="left", fontsize=11, color=palette(num))
    for s in ["top", "right"]: ax.spines[s].set_visible(False)

fig.suptitle("How the nine largest owners built their Davidson portfolios\n"
             "corporate SFR parcels acquired per year",
             fontsize=14, style="italic", x=0.09, ha="left", y=1.0)
fig.text(0.5, 0.04, "Acquisition year", ha="center", fontsize=12)
fig.text(0.06, 0.5, "Parcels acquired", va="center", rotation=90, fontsize=12)
fig.tight_layout(rect=[0.02, 0.05, 1, 0.95])
plt.savefig(os.path.join(os.path.dirname(__file__), "32_small_multiples_lines.png"), dpi=150)
print("wrote 32_small_multiples_lines.png")
