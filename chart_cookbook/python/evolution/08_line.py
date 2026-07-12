"""
Line chart — EVOLUTION
A value over time. Inspired by python-graph-gallery.com.
"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

df = pd.DataFrame({
    "year": list(range(2013, 2026)),
    "corporate_acquisitions": [210, 340, 520, 690, 880, 1010, 1180, 1360, 1720, 1980, 1540, 1120, 860],
})

sns.set_style("whitegrid")
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(df["year"], df["corporate_acquisitions"], marker="o", color="#1c458c", lw=2)
ax.set_title("Corporate SF Acquisitions per Year", fontweight="bold")
ax.set_xlabel("Year"); ax.set_ylabel("Parcels acquired")
sns.despine()
plt.tight_layout()
plt.savefig("08_line.png", dpi=150)
