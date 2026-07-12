"""
Density (KDE) plot — DISTRIBUTION
Smoothed distribution; good for comparing groups. Inspired by python-graph-gallery.com.
"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

rng = np.random.default_rng(7)
df = pd.DataFrame({
    "sale_price_k": np.concatenate([rng.normal(320, 60, 1000), rng.normal(430, 90, 1000)]),
    "buyer": ["Individual"] * 1000 + ["Corporate"] * 1000,
})

sns.set_style("whitegrid")
fig, ax = plt.subplots(figsize=(8, 4.5))
sns.kdeplot(data=df, x="sale_price_k", hue="buyer", fill=True, alpha=0.4,
            palette=["#4fa0bd", "#e6194b"], ax=ax)
ax.set_title("Sale Price Density by Buyer Type", fontweight="bold")
ax.set_xlabel("Sale price ($000s)")
sns.despine()
plt.tight_layout()
plt.savefig("12_density_kde.png", dpi=150)
