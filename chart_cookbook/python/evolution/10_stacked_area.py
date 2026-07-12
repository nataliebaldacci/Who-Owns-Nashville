"""
Stacked area chart — EVOLUTION
Composition over time. Inspired by python-graph-gallery.com.
"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

years = list(range(2018, 2026))
df = pd.DataFrame({
    "year": years,
    "Progress": [60, 110, 180, 260, 340, 300, 250, 220],
    "AMH":      [80, 130, 190, 250, 320, 280, 210, 180],
    "Amherst":  [40, 70, 120, 170, 230, 190, 150, 120],
})

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.stackplot(df["year"], df["Progress"], df["AMH"], df["Amherst"],
             labels=["Progress", "AMH", "Amherst"],
             colors=["#e6194b", "#2166ac", "#1a9850"], alpha=0.9)
ax.set_title("Acquisitions by Operator over Time", fontweight="bold")
ax.set_xlabel("Year"); ax.set_ylabel("Parcels acquired")
ax.legend(loc="upper left", frameon=True)
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)
plt.tight_layout()
plt.savefig("10_stacked_area.png", dpi=150)
