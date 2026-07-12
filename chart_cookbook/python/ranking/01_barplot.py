"""
Basic bar plot — RANKING
Style inspired by the Python Graph Gallery (python-graph-gallery.com).
Swap the sample DataFrame for your own (e.g. owner_leaderboard.json).
"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# --- sample data (housing-themed) ---
df = pd.DataFrame({
    "operator": ["Progress", "AMH", "Amherst", "Regent", "Normandy", "CRG/ECG", "Tricon", "RSD"],
    "parcels":  [1215, 1182, 699, 642, 348, 303, 298, 263],
})

sns.set_style("whitegrid")
fig, ax = plt.subplots(figsize=(8, 4.5))
sns.barplot(data=df, x="operator", y="parcels", color="#1c458c", ax=ax)
ax.set_title("Largest Corporate Operators — Parcels Held", fontweight="bold")
ax.set_xlabel(""); ax.set_ylabel("Parcels")
plt.xticks(rotation=45, ha="right")
sns.despine()
plt.tight_layout()
plt.savefig("01_barplot.png", dpi=150)
