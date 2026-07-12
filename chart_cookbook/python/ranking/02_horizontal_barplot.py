"""
Horizontal bar plot — RANKING
Best when category labels are long. Inspired by python-graph-gallery.com.
"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

df = pd.DataFrame({
    "operator": ["Progress Residential", "American Homes 4 Rent", "Amherst Residential",
                 "Regent Homes", "Normandy Group", "CRG / ECG", "Tricon Residential", "RSD Development"],
    "parcels":  [1215, 1182, 699, 642, 348, 303, 298, 263],
}).sort_values("parcels")

sns.set_style("whitegrid")
fig, ax = plt.subplots(figsize=(8, 4.5))
sns.barplot(data=df, y="operator", x="parcels", color="#4fa0bd", ax=ax)
ax.set_title("Largest Corporate Operators", fontweight="bold")
ax.set_ylabel(""); ax.set_xlabel("Parcels held")
sns.despine()
plt.tight_layout()
plt.savefig("02_horizontal_barplot.png", dpi=150)
