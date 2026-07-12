"""Boundaries overview — MAP. All Davidson boundary layers side by side, so you
can see the geography options for any choropleth (census + local)."""
import matplotlib; matplotlib.use("Agg")
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import matplotlib.pyplot as plt
from styles.boundaries import load, BOUNDARIES
layers = ["tract", "blockgroup", "community", "council", "zip"]
fig, axes = plt.subplots(1, len(layers), figsize=(20, 4.6))
for ax, name in zip(axes, layers):
    g = load(name)
    g.plot(ax=ax, facecolor="#eef4fb", edgecolor="#1c458c", linewidth=0.4)
    ax.set_title(f"{name}  (n={len(g)})", fontweight="bold", fontsize=11); ax.axis("off")
fig.suptitle("Davidson County boundary layers available to the cookbook",
             fontsize=14, fontweight="bold")
plt.tight_layout(rect=[0, 0, 1, .95]); plt.savefig("30_boundaries_overview.png", dpi=130)
print("wrote 30_boundaries_overview.png")
