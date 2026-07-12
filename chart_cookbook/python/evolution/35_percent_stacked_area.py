"""Percent (100%) stacked area chart (python-graph-gallery style). Each year's
values are normalized to sum to 100%, so the chart reads as a changing MIX
rather than a growing total. Real data: the build-era composition of corporate
SFR acquisitions in Davidson County by acquisition year (pre-1980, 1980-1999,
2000+), showing corporate buyers shifting toward newer stock over time."""
import matplotlib; matplotlib.use("Agg")
import os, json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
props = [f["properties"] for f in
         json.load(open(os.path.join(ROOT, "Davidson_Active_Corporate_SFR_Detail.geojson")))["features"]]

def era(y):
    return "Built 2000+" if y >= 2000 else ("Built 1980-1999" if y >= 1980 else "Built pre-1980")

recs = []
for p in props:
    a, yb = str(p.get("acq", ""))[:4], str(p.get("ybuilt", ""))
    if a.isdigit() and yb.isdigit() and 2012 <= int(a) <= 2025:
        recs.append((int(a), era(int(yb))))
df = pd.DataFrame(recs, columns=["year", "era"])
counts = df.groupby(["year", "era"]).size().unstack(fill_value=0)
order = ["Built pre-1980", "Built 1980-1999", "Built 2000+"]
counts = counts.reindex(columns=order, fill_value=0)
pct = counts.divide(counts.sum(axis=1), axis=0) * 100   # normalize each year to 100%
years = pct.index.to_numpy()

COLORS = ["#dcc7a1", "#4fa0bd", "#1c458c"]
fig, ax = plt.subplots(figsize=(11, 7))
ax.stackplot(years, [pct[c] for c in order], labels=order, colors=COLORS, alpha=0.92)
ax.set_xlim(years.min(), years.max()); ax.set_ylim(0, 100)
ax.set_ylabel("Share of that year's acquisitions (%)")
ax.set_xlabel("Acquisition year")
ax.margins(x=0)
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)

# inline labels at the right edge, centered in each band
right = pct.iloc[-1]
cum = 0
for c, col in zip(order, COLORS):
    mid = cum + right[c] / 2
    ax.text(years.max() + 0.15, mid, f"{c}\n{right[c]:.0f}%", va="center", ha="left",
            fontsize=10, fontweight="bold", color="#20303f")
    cum += right[c]
ax.set_xlim(years.min(), years.max() + 2.6)

ax.set_title("What era of housing did corporate buyers acquire?\n"
             "Build-era mix of Davidson corporate SFR acquisitions, normalized to 100% each year",
             fontsize=13, loc="left")
fig.text(0.09, 0.02, "Source: Who Owns Nashville, Davidson County active corporate SFR detail",
         fontsize=8, color="#5a5a5a")
plt.tight_layout(rect=[0, 0.03, 1, 1])
plt.savefig(os.path.join(os.path.dirname(__file__), "35_percent_stacked_area.png"), dpi=150)
print("wrote 35_percent_stacked_area.png  (%d years)" % len(years))
