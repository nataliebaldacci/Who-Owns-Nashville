"""
Cleveland dot plot — RANKING (two series compared)
Compares two values per category (e.g. TN vs out-of-state). Inspired by python-graph-gallery.com.
"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

df = pd.DataFrame({
    "operator": ["Progress", "AMH", "Amherst", "Regent", "Normandy", "Tricon", "Starwood"],
    "in_state": [290, 274, 204, 584, 346, 65, 21],
    "out_state":[925, 908, 490, 12, 2, 233, 231],
}).sort_values("out_state")

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.hlines(y=df["operator"], xmin=df["in_state"], xmax=df["out_state"], color="#c8c7c7", lw=2, zorder=1)
ax.scatter(df["in_state"], df["operator"], color="#f0af1e", s=70, label="In-state (TN)", zorder=2)
ax.scatter(df["out_state"], df["operator"], color="#1c458c", s=70, label="Out-of-state", zorder=2)
ax.set_title("Holdings by Owner Location", fontweight="bold")
ax.set_xlabel("Parcels")
ax.legend(frameon=True)
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)
plt.tight_layout()
plt.savefig("04_cleveland_dotplot.png", dpi=150)
