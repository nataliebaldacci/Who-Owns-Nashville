"""
Histogram — DISTRIBUTION
Shape of a single numeric variable. Inspired by python-graph-gallery.com.
"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
df = pd.DataFrame({"sale_price_k": rng.lognormal(mean=5.9, sigma=0.4, size=2000)})

sns.set_style("whitegrid")
fig, ax = plt.subplots(figsize=(8, 4.5))
sns.histplot(df["sale_price_k"], bins=40, color="#1c458c", ax=ax)
ax.set_title("Distribution of SF Sale Prices ($000s)", fontweight="bold")
ax.set_xlabel("Sale price ($000s)"); ax.set_ylabel("Count")
sns.despine()
plt.tight_layout()
plt.savefig("11_histogram.png", dpi=150)
