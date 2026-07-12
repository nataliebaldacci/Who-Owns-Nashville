"""
Scatter plot — CORRELATION
Relationship between two numeric variables. Inspired by python-graph-gallery.com.
"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

rng = np.random.default_rng(5)
sqft = rng.normal(1900, 400, 500)
price = sqft * 0.22 + rng.normal(0, 40, 500)
df = pd.DataFrame({"sqft": sqft, "price_k": price})

sns.set_style("whitegrid")
fig, ax = plt.subplots(figsize=(7, 5))
sns.scatterplot(data=df, x="sqft", y="price_k", color="#1c458c", alpha=0.5, ax=ax)
ax.set_title("Sale Price vs Home Size", fontweight="bold")
ax.set_xlabel("Living area (sqft)"); ax.set_ylabel("Sale price ($000s)")
sns.despine()
plt.tight_layout()
plt.savefig("15_scatter.png", dpi=150)
