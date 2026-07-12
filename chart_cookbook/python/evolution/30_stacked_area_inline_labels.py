"""Smoothed stacked area with inline labels (Gilbert Fontana wealth-chart style).
Ownership composition over time, spline-smoothed, custom palette, big title,
year total callouts, and right-side category labels."""
import matplotlib; matplotlib.use("Agg")
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
years = np.arange(2000, 2025, 2)
rng = np.random.default_rng(2)
cats = ["Owner-occupied","Individual investor","Local LLC","Corporate","REIT","Trust","Other"]
COLORS = ["#003f5c","#2f4b7c","#665191","#a05195","#d45087","#ff7c43","#ffa600"]
base = np.array([120,25,18,8,3,10,16], dtype=float)
data = {}
for i, c in enumerate(cats):
    drift = np.linspace(0, rng.uniform(-30, 40), len(years))
    data[c] = np.clip(base[i] + drift + rng.normal(0, 2, len(years)), 1, None)
df = pd.DataFrame(data, index=years)
xs = np.linspace(years.min(), years.max(), 300)
sm = pd.DataFrame({c: make_interp_spline(years, df[c])(xs) for c in cats})
fig, ax = plt.subplots(figsize=(11, 8))
ax.stackplot(xs, sm.values.T, colors=COLORS)
tot = sm.sum(axis=1)
for yr in [2000, 2008, 2016, 2024]:
    j = int(np.argmin(np.abs(xs - yr)))
    ax.plot([xs[j], xs[j]], [0, tot[j]*1.04], color="black", lw=1)
    ax.plot(xs[j], tot[j]*1.04, "o", color="black", ms=4)
    ax.text(xs[j]-0.4, tot[j]*1.06, f"{tot[j]:.0f}k", weight="bold", size=9)
ends = sm.iloc[-1]; cum = 0
for c, col in zip(cats, COLORS):
    ax.text(2024.4, cum + ends[c]/2, c, color=col, weight="bold", size=9, va="center"); cum += ends[c]
ax.text(2000, tot.max()*0.72, "Ownership\ncomposition\nof Davidson\nhousing", size=26, weight="bold")
for sp in ["left","right","top"]: ax.spines[sp].set_visible(False)
ax.tick_params(left=False, labelleft=False); ax.set_xlim(2000, 2028)
ax.text(2000, -tot.max()*0.06, "Illustrative composition · Who Owns Nashville", size=8, color="#555")
plt.tight_layout(); plt.savefig("30_stacked_area_inline_labels.png", dpi=150)
print("wrote 30_stacked_area_inline_labels.png")
