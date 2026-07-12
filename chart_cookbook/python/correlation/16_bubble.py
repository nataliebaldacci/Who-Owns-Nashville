"""
Bubble chart — CORRELATION
Scatter with a third variable encoded as marker size. Inspired by python-graph-gallery.com.
"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

df = pd.DataFrame({
    "operator": ["Progress", "AMH", "Amherst", "Regent", "Normandy", "Tricon"],
    "parcels":  [1215, 1182, 699, 642, 348, 298],
    "avg_value_k": [373, 434, 448, 190, 433, 439],
    "dwelling_units": [1198, 1039, 857, 100, 372, 290],
})
colors = ["#e6194b", "#2166ac", "#1a9850", "#f0af1e", "#911eb4", "#4fa0bd"]

fig, ax = plt.subplots(figsize=(7.5, 5))
ax.scatter(df["parcels"], df["avg_value_k"], s=df["dwelling_units"], c=colors, alpha=0.7, edgecolor="white")
for _, r in df.iterrows():
    ax.annotate(r["operator"], (r["parcels"], r["avg_value_k"]), fontsize=9,
                ha="center", va="center")
ax.set_title("Operators — Parcels vs Avg Value (size = dwelling units)", fontweight="bold")
ax.set_xlabel("Parcels held"); ax.set_ylabel("Avg parcel value ($000s)")
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)
plt.tight_layout()
plt.savefig("16_bubble.png", dpi=150)
