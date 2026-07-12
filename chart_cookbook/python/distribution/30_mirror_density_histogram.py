"""Mirror density + histogram (python-graph-gallery style): compare two
distributions back-to-back around a zero baseline. Real data — corporate SFR
acquisitions in Davidson County by acquisition year, split by home vintage:
homes built 2000 or later (top, blue) vs built before 2000 (bottom, orange).
The mirror shows corporate buyers shifting from older scattered stock toward
newer build-to-rent product. Left panel = density, right panel = histogram."""
import matplotlib; matplotlib.use("Agg")
import os, json
import numpy as np
from numpy import linspace
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

BLUE, ORANGE = "#1c458c", "#f0af1e"
ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
props = [f["properties"] for f in
         json.load(open(os.path.join(ROOT, "Davidson_Active_Corporate_SFR_Detail.geojson")))["features"]]

def acq_years(pred):
    out = []
    for p in props:
        a, yb = str(p.get("acq", "")), str(p.get("ybuilt", ""))
        if a[:4].isdigit() and yb.isdigit() and 2010 <= int(a[:4]) <= 2026 and pred(int(yb)):
            out.append(int(a[:4]))
    return np.array(out)

new = acq_years(lambda y: y >= 2000)   # newer / BTR-era stock
old = acq_years(lambda y: y < 2000)    # pre-2000 existing stock

fig, (axd, axh) = plt.subplots(1, 2, figsize=(14, 7))

# --- left: mirror density ---
sns.kdeplot(x=new, ax=axd, fill=True, alpha=0.9, color=BLUE, bw_adjust=1.2)
kde = gaussian_kde(old)
xr = linspace(old.min(), old.max(), len(old))
axd.plot(xr, -kde(xr), color=ORANGE)
axd.fill_between(xr, -kde(xr), color=ORANGE, alpha=0.9)
axd.axhline(0, color="black", lw=1)
axd.set_xlabel("Acquisition year"); axd.set_ylabel("Density")
axd.set_title("Mirror density", loc="left", fontweight="bold")
axd.text(2011, 0.06, "Built 2000+", color=BLUE, fontweight="bold")
axd.text(2011, -0.06, "Built pre-2000", color=ORANGE, fontweight="bold")

# --- right: mirror histogram ---
bins = np.arange(2010.5, 2027.5, 1)
sns.histplot(x=new, stat="count", bins=bins, ax=axh, color=BLUE, edgecolor="black")
heights, edges = np.histogram(old, bins=bins)
width = np.diff(edges)[0]
pos = edges[:-1] + width / 2
axh.bar(pos, -heights, width=width, color=ORANGE, edgecolor="black")
axh.axhline(0, color="black", lw=1)
axh.set_xlabel("Acquisition year"); axh.set_ylabel("Parcels acquired")
axh.set_title("Mirror histogram", loc="left", fontweight="bold")

fig.suptitle("When corporate buyers acquired Davidson homes, by vintage",
             fontsize=16, fontweight="bold", x=0.09, ha="left")
fig.text(0.09, 0.93, "Newer stock (built 2000+) was acquired later and faster than pre-2000 homes",
         fontsize=11, color="#5a5a5a", ha="left")
fig.text(0.09, 0.01, "Source: Who Owns Nashville, Davidson County active corporate SFR detail",
         fontsize=9, color="#5a5a5a")
plt.tight_layout(rect=[0, 0.02, 1, 0.92])
plt.savefig(os.path.join(os.path.dirname(__file__), "30_mirror_density_histogram.png"), dpi=150)
print("wrote 30_mirror_density_histogram.png  (new=%d, old=%d)" % (len(new), len(old)))
