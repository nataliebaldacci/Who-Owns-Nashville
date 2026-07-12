"""
Lollipop chart — RANKING
A lighter alternative to bars. Inspired by python-graph-gallery.com.
"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

df = pd.DataFrame({
    "operator": ["Progress", "AMH", "Amherst", "Regent", "Normandy", "CRG/ECG", "Tricon", "RSD"],
    "parcels":  [1215, 1182, 699, 642, 348, 303, 298, 263],
}).sort_values("parcels")

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.hlines(y=df["operator"], xmin=0, xmax=df["parcels"], color="#c8c7c7", lw=2)
ax.plot(df["parcels"], df["operator"], "o", color="#f0af1e", markersize=9)
ax.set_title("Corporate Operators — Parcels Held", fontweight="bold")
ax.set_xlabel("Parcels")
for spine in ["top", "right"]:
    ax.spines[spine].set_visible(False)
plt.tight_layout()
plt.savefig("03_lollipop.png", dpi=150)
