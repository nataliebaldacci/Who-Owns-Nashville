"""Ridgeline — DISTRIBUTION. Many groups' distributions stacked (price per year)."""
import matplotlib; matplotlib.use("Agg")
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import matplotlib.pyplot as plt, numpy as np
from styles.won_styles import apply_style
apply_style("jchs")
rng = np.random.default_rng(1); years = list(range(2016, 2025))
fig, axes = plt.subplots(len(years), 1, figsize=(8, 5), sharex=True)
xs = np.linspace(100, 700, 300)
for i, (ax, yr) in enumerate(zip(axes, years)):
    mu = 300 + i*22; d = rng.normal(mu, 70, 800)
    from numpy import histogram
    h, e = histogram(d, bins=xs, density=True)
    ax.fill_between(e[:-1], h, color="#508DA6", alpha=.8, lw=.8, edgecolor="white")
    ax.set_yticks([]); ax.set_ylabel(str(yr), rotation=0, ha="right", va="center", fontsize=9)
    for s in ax.spines.values(): s.set_visible(False)
axes[-1].set_xlabel("Sale price ($000s)")
fig.suptitle("Sale Price Distribution by Year (ridgeline)", fontweight="bold")
plt.tight_layout(); plt.savefig("21_ridgeline.png", dpi=150)
