"""
Area chart — EVOLUTION
Line with filled area to emphasize magnitude. Inspired by python-graph-gallery.com.
"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

df = pd.DataFrame({
    "year": list(range(2013, 2026)),
    "corporate_acquisitions": [210, 340, 520, 690, 880, 1010, 1180, 1360, 1720, 1980, 1540, 1120, 860],
})

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.fill_between(df["year"], df["corporate_acquisitions"], color="#4fa0bd", alpha=0.4)
ax.plot(df["year"], df["corporate_acquisitions"], color="#1c458c", lw=2)
ax.set_title("Corporate SF Acquisitions per Year", fontweight="bold")
ax.set_xlabel("Year"); ax.set_ylabel("Parcels acquired")
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)
plt.tight_layout()
plt.savefig("09_area.png", dpi=150)
