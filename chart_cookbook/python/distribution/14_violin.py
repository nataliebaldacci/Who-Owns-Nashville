"""
Violin plot — DISTRIBUTION
Box plot + density silhouette. Inspired by python-graph-gallery.com.
"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

rng = np.random.default_rng(11)
groups = ["Individual", "Corporate", "Trust", "Bank"]
df = pd.concat([
    pd.DataFrame({"buyer": g, "sale_price_k": rng.normal(m, s, 400)})
    for g, m, s in zip(groups, [310, 440, 360, 500], [70, 110, 80, 130])
])

sns.set_style("whitegrid")
fig, ax = plt.subplots(figsize=(8, 4.5))
sns.violinplot(data=df, x="buyer", y="sale_price_k",
               palette=["#4fa0bd", "#e6194b", "#911eb4", "#16a085"], ax=ax)
ax.set_title("Sale Price Distribution by Buyer Type", fontweight="bold")
ax.set_xlabel(""); ax.set_ylabel("Sale price ($000s)")
sns.despine()
plt.tight_layout()
plt.savefig("14_violin.png", dpi=150)
