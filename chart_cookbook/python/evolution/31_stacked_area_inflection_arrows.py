"""Stacked area with inline labels + inflection arrows (Joseph Barbier natural-
disasters style). Ownership composition over years, custom palette, right-side
inline labels, and drawarrow arrows (some with an inflection point) linking each
band to its label."""
import matplotlib; matplotlib.use("Agg")
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from drawarrow import ax_arrow
years = np.arange(1990, 2025)
rng = np.random.default_rng(7)
cats = ["Owner-occupied","Individual","Local LLC","Corporate","REIT","Trust","Other"]
COLORS = ["#264653","#2a9d8f","#8ab17d","#e9c46a","#f4a261","#e76f51","#b5838d"]
base = [140,40,22,10,4,14,18]
df = pd.DataFrame({c: np.clip(np.array(b, float) + np.linspace(0, rng.uniform(-30,45), len(years)) + rng.normal(0,2,len(years)), 1, None)
                   for c,b in zip(cats, base)}, index=years)
order = df.sum().sort_values().index.tolist()
fig, ax = plt.subplots(figsize=(13, 7)); ax.set_axis_off()
ax.stackplot(years, np.stack([df[c] for c in order], -1).T, colors=[COLORS[cats.index(c)] for c in order])
for yr in range(1990, 2030, 10):
    ax.text(yr, -12, str(yr), color="grey", fontsize=11, ha="left", va="top")
tot = df.sum(axis=1)
cum = 0; ends = df.iloc[-1]
label_y = {}
for c in order:
    label_y[c] = cum + ends[c]/2; cum += ends[c]
for c in order:
    y = label_y[c]
    ax.text(2026.5, y, f"{c.upper()} — {int(ends[c])}", color=COLORS[cats.index(c)], fontsize=10, weight="bold", va="center")
    ax_arrow(tail_position=(2024, y), head_position=(2026, y), clip_on=False, color="grey", fill_head=False,
             inflection_position=(2025, y+6) if ends[c] < 30 else None)
ax.text(1990, tot.max()*1.02, "Ownership composition of Davidson housing, 1990-2024",
        fontsize=18, weight="bold")
ax.text(1990, -22, "Illustrative composition  ·  Viz: Who Owns Nashville", fontsize=9, color="#555")
ax.set_xlim(1990, 2032)
plt.savefig("31_stacked_area_inflection_arrows.png", dpi=150, bbox_inches="tight")
print("wrote 31_stacked_area_inflection_arrows.png")
