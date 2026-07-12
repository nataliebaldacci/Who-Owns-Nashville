"""Subplot layout reference (matplotlib subplot / subplots / subplot2grid).
A practical cheatsheet: a composed mini-dashboard using subplot2grid custom
proportions, plus the layout recipes in the docstring. Wired to Nashville data.

Layout recipes (see matplotlib.pyplot):
  plt.subplot(121)                 # 1 row, 2 cols, panel 1  (3-digit RCP code)
  plt.subplot(212)                 # 2 rows, 1 col, panel 2
  fig, ax = plt.subplots(2, 2, sharex=True, sharey=True)   # grid, shared axes
  ax = plt.subplot2grid((2,2),(0,0), colspan=2)            # span cells
  fig.suptitle(...); ax.set_title(..., loc="left")         # figure + panel titles
"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np

ops = ["Progress","AMH","Amherst","Regent","Normandy","Tricon"]
parcels = [1215,1182,699,642,348,298]
years = np.arange(2013, 2025)
acq = np.cumsum(np.abs(np.diff(np.r_[0, np.linspace(0, 2000, len(years)+1)])))[:len(years)]
rng = np.random.default_rng(5); prices = rng.lognormal(np.log(400), 0.5, 4000)

fig = plt.figure(figsize=(11, 7))
# top row spans both columns
ax1 = plt.subplot2grid((2, 2), (0, 0), colspan=2)
ax1.plot(years, acq, marker="o", color="#1c458c"); ax1.fill_between(years, acq, color="#4fa0bd", alpha=.3)
ax1.set_title("Cumulative acquisitions", loc="left", style="italic", color="grey")
# bottom-left
ax2 = plt.subplot2grid((2, 2), (1, 0))
ax2.bar(ops, parcels, color="#f0af1e"); ax2.set_xticklabels(ops, rotation=45, ha="right", fontsize=8)
ax2.set_title("Operators by parcels", loc="left", style="italic", color="grey")
# bottom-right
ax3 = plt.subplot2grid((2, 2), (1, 1))
ax3.hist(prices, bins=30, color="#1a9850"); ax3.set_title("Price distribution", loc="left", style="italic", color="grey")
for ax in (ax1, ax2, ax3):
    for sp in ["top","right"]: ax.spines[sp].set_visible(False)
fig.suptitle("Composed dashboard via subplot2grid (top row spans 2 columns)", y=1.0, fontweight="bold")
plt.tight_layout()
plt.savefig("subplot_layouts.png", dpi=150, bbox_inches="tight")
print("wrote subplot_layouts.png")
