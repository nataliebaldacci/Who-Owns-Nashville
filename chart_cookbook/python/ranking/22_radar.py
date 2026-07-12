"""Radar / spider — RANKING. One or two entities across several metrics."""
import matplotlib; matplotlib.use("Agg")
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import matplotlib.pyplot as plt, numpy as np
from styles.won_styles import apply_style, palette
apply_style("jchs"); c = palette("jchs")
labels = ["Parcels", "Out-of-state %", "Avg value", "Dwelling units", "Acreage"]
prog = [0.95, 0.76, 0.70, 0.98, 0.35]; amh = [0.92, 0.77, 0.82, 0.85, 0.42]
ang = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist(); ang += ang[:1]
fig, ax = plt.subplots(figsize=(6.5, 6), subplot_kw=dict(polar=True))
for vals, name, col in [(prog, "Progress", c[0]), (amh, "AMH", c[1])]:
    v = vals + vals[:1]
    ax.plot(ang, v, color=col, lw=2, label=name); ax.fill(ang, v, color=col, alpha=.15)
ax.set_xticks(ang[:-1]); ax.set_xticklabels(labels, fontsize=9); ax.set_yticklabels([])
ax.set_title("Operator Profiles (normalized)", fontweight="bold", pad=18)
ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.1), frameon=True)
plt.tight_layout(); plt.savefig("22_radar.png", dpi=150)
