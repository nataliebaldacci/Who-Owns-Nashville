"""CRS 'Total Housing Units' style (R48892 Fig 1): tan bars for the level,
blue line for the units-to-population ratio on a right axis. Dual-axis.
Swap the sample series for Davidson totals + population."""
import matplotlib; matplotlib.use("Agg")
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import matplotlib.pyplot as plt, numpy as np
from styles.won_styles import apply_style, ACCENTS
apply_style("crs")
yrs = np.arange(1980, 2025)
units = np.linspace(88, 148, len(yrs)) * 1000            # thousands
ratio = 0.52 + 0.06*np.sin(np.linspace(0, 3, len(yrs))) + np.linspace(0, .04, len(yrs))
fig, ax = plt.subplots(figsize=(9, 4.6))
ax.bar(yrs, units, color=ACCENTS["crs_tan"], width=.8, label="Thousands of Housing Units")
ax.set_ylabel(""); ax.set_ylim(0, 160000); ax.grid(False)
ax2 = ax.twinx()
ax2.plot(yrs, ratio, color=ACCENTS["crs_blue"], lw=2.2, label="Housing Units to Population Ratio")
ax2.set_ylim(0.4, 0.8); ax2.grid(False)
ax.set_title("Total Housing Units", fontweight="bold", loc="left")
fig.legend(loc="upper center", ncol=2, frameon=False, fontsize=9, bbox_to_anchor=(.5, 1.02))
plt.tight_layout(); plt.savefig("crs_total_housing_units.png", dpi=150)
