"""Renders the same bar, line, and stacked-bar in three house styles
(WON, JCHS, CRS) so you can compare the color systems side by side."""
import matplotlib; matplotlib.use("Agg")
import os, sys; sys.path.insert(0, os.path.dirname(__file__))
import matplotlib.pyplot as plt, numpy as np
from styles.won_styles import palette
styles = ["won", "jchs", "crs"]; titles = {"won":"Who Owns Nashville","jchs":"Harvard JCHS","crs":"CRS report"}
ops = ["Progress","AMH","Amherst","Regent"]; par = [1215,1182,699,642]
yrs = list(range(2018, 2025)); line = [880,1010,1180,1360,1720,1980,1540]
tn = [290,274,204,584]; oos = [925,908,490,12]
fig, axes = plt.subplots(3, 3, figsize=(12, 9))
for r, st in enumerate(styles):
    c = palette(st)
    a0, a1, a2 = axes[r]
    a0.bar(ops, par, color=c[0]); a0.set_title(f"{titles[st]} — bar", fontsize=10, fontweight="bold")
    a1.plot(yrs, line, color=c[1] if st!='crs' else c[0], lw=2, marker="o"); a1.set_title("line", fontsize=10)
    a2.bar(ops, tn, color=c[3] if st=='won' else c[0]); a2.bar(ops, oos, bottom=tn, color=c[0] if st=='won' else c[1])
    a2.set_title("stacked", fontsize=10)
    for a in axes[r]:
        a.tick_params(labelsize=8)
        for s in ["top","right"]: a.spines[s].set_visible(False)
        a.grid(axis="y", color="#e6e6e6")
        for lab in a.get_xticklabels(): lab.set_rotation(30); lab.set_ha("right")
fig.suptitle("House-style comparison — same data, three palettes", fontsize=13, fontweight="bold")
plt.tight_layout(rect=[0,0,1,.97]); plt.savefig("figures/style_showcase.png", dpi=130)
