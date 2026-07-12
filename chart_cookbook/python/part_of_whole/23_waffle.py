"""Waffle — PART OF WHOLE. Share of a total as a 10x10 grid of squares."""
import matplotlib; matplotlib.use("Agg")
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import matplotlib.pyplot as plt, numpy as np
from styles.won_styles import apply_style, palette
apply_style("jchs"); c = palette("jchs")
cats = ["Individual", "Corporate", "Trust", "Other"]; shares = [90, 7, 2, 1]
grid = np.zeros((10, 10), int); idx = 0
for ci, n in enumerate(shares):
    for _ in range(n):
        grid[idx % 10, idx // 10] = ci; idx += 1
fig, ax = plt.subplots(figsize=(6.5, 6))
for x in range(10):
    for y in range(10):
        ax.add_patch(plt.Rectangle((x, y), .9, .9, color=c[grid[y, x]]))
ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.set_aspect("equal"); ax.axis("off")
ax.set_title("Owner Type — Each Square = 1% of Owners", fontweight="bold")
handles = [plt.Rectangle((0,0),1,1,color=c[i]) for i in range(len(cats))]
ax.legend(handles, [f"{l} ({s}%)" for l,s in zip(cats,shares)], loc="upper center",
          bbox_to_anchor=(.5,-.02), ncol=4, frameon=False, fontsize=9)
plt.tight_layout(); plt.savefig("23_waffle.png", dpi=150)
