"""
Treemap — PART OF WHOLE
Nested rectangles sized by value. Needs `squarify`. Inspired by python-graph-gallery.com.
"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import squarify
import pandas as pd

df = pd.DataFrame({
    "operator": ["Progress", "AMH", "Amherst", "Regent", "Normandy", "Other"],
    "parcels":  [1215, 1182, 699, 642, 348, 900],
})
colors = ["#e6194b", "#2166ac", "#1a9850", "#f0af1e", "#911eb4", "#c8c7c7"]

fig, ax = plt.subplots(figsize=(8, 5))
squarify.plot(sizes=df["parcels"],
              label=[f"{o}\n{v:,}" for o, v in zip(df["operator"], df["parcels"])],
              color=colors, text_kwargs={"color": "white", "fontsize": 10}, ax=ax)
ax.set_title("Share of Corporate-Owned Parcels", fontweight="bold")
ax.axis("off")
plt.tight_layout()
plt.savefig("06_treemap.png", dpi=150)
