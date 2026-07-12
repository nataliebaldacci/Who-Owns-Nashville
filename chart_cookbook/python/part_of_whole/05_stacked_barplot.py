"""
Stacked bar plot — PART OF WHOLE
Composition within each category. Inspired by python-graph-gallery.com.
"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

df = pd.DataFrame({
    "operator": ["Progress", "AMH", "Amherst", "Regent", "Normandy", "Tricon"],
    "in_state": [290, 274, 204, 584, 346, 65],
    "out_state":[925, 908, 490, 12, 2, 233],
})

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.bar(df["operator"], df["in_state"], label="In-state (TN)", color="#f0af1e")
ax.bar(df["operator"], df["out_state"], bottom=df["in_state"], label="Out-of-state", color="#1c458c")
ax.set_title("In-State vs Out-of-State Holdings", fontweight="bold")
ax.set_ylabel("Parcels"); ax.legend(frameon=True)
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)
plt.tight_layout()
plt.savefig("05_stacked_barplot.png", dpi=150)
