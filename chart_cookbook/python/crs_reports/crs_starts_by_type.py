"""CRS/HUD 'Housing Starts by Type' style: stacked area, orange=SF,
grey=MF for sale, gold=MF for rent, per 1,000 population."""
import matplotlib; matplotlib.use("Agg")
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import matplotlib.pyplot as plt, numpy as np
from styles.won_styles import apply_style, palette
apply_style("crs"); c = palette("crs")
yrs = np.arange(1980, 2023)
n = len(yrs); rng = np.random.default_rng(4)
sf = 5 + 1.5*np.sin(np.linspace(0, 6, n)) - np.linspace(0, 1.5, n)
sf = np.clip(sf, 1.8, None)
mfs = np.clip(0.8 + 0.5*np.sin(np.linspace(1, 7, n)), 0.2, None)
mfr = np.clip(1.2 + 0.7*np.sin(np.linspace(2, 8, n)) + np.linspace(0, .5, n), 0.3, None)
fig, ax = plt.subplots(figsize=(9, 4.8))
ax.stackplot(yrs, sf, mfs, mfr, colors=[c[1], c[2], c[3]],
             labels=["Single Family", "Multifamily for Sale", "Multifamily for Rent"])
ax.set_ylabel("Starts Per Thousand Population")
ax.set_title("Housing Starts by Type", fontweight="bold", loc="left")
ax.legend(loc="upper center", ncol=3, frameon=False, bbox_to_anchor=(.5, -.12))
ax.grid(False)
plt.tight_layout(); plt.savefig("crs_starts_by_type.png", dpi=150)
