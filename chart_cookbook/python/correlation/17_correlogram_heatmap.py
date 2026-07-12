"""
Correlogram / heatmap — CORRELATION
Correlation matrix as a colored grid. Inspired by python-graph-gallery.com.
"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

rng = np.random.default_rng(9)
n = 300
sqft = rng.normal(1900, 400, n)
df = pd.DataFrame({
    "sqft": sqft,
    "price_k": sqft * 0.22 + rng.normal(0, 40, n),
    "year_built": rng.normal(1995, 20, n),
    "lot_acres": rng.normal(0.28, 0.1, n),
})
corr = df.corr()

fig, ax = plt.subplots(figsize=(6.5, 5.5))
sns.heatmap(corr, annot=True, cmap="RdYlBu_r", center=0, fmt=".2f", square=True,
            linewidths=0.5, cbar_kws={"shrink": 0.8}, ax=ax)
ax.set_title("Correlation of Parcel Attributes", fontweight="bold")
plt.tight_layout()
plt.savefig("17_correlogram_heatmap.png", dpi=150)
