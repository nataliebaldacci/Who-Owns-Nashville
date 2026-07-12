"""Timeseries — EVOLUTION. Proper datetime x-axis with monthly data."""
import matplotlib; matplotlib.use("Agg")
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import matplotlib.pyplot as plt, pandas as pd, numpy as np
import matplotlib.dates as mdates
from styles.won_styles import apply_style, palette
apply_style("crs"); c = palette("crs")
idx = pd.date_range("2019-01-01", "2024-12-01", freq="MS")
rng = np.random.default_rng(2)
val = 100 + np.cumsum(rng.normal(0, 4, len(idx)))
s = pd.Series(val, index=idx)
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(s.index, s.values, color=c[0], lw=1.8)
ax.xaxis.set_major_locator(mdates.YearLocator()); ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax.set_title("Monthly Corporate Acquisitions Index", fontweight="bold"); ax.set_ylabel("Index")
plt.tight_layout(); plt.savefig("26_timeseries.png", dpi=150)
