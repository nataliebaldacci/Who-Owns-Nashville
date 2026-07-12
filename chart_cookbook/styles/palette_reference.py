"""Draw a browsable swatch sheet of representative palettes across every
library the cookbook can reach. Run: python styles/palette_reference.py
Writes figures/palette_reference.png."""
import matplotlib; matplotlib.use("Agg")
import os, sys; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from styles.palettes import get

GROUPS = {
    "Cookbook house styles": ["won", "hud", "jchs", "crs"],
    "Categorical (qualitative)": ["Category10", "Category20", "Set2", "Bold", "Prism", "Pastel", "Antique", "Acadia"],
    "Sequential (choropleth)": ["YlOrBr", "Blues", "Greens", "Thermal", "viridis", "cividis", "magma"],
    "Diverging (change / gain-loss)": ["RdYlBu", "RdBu", "BrBG", "Balance", "coolwarm", "Spectral"],
}
rows = sum(len(v) for v in GROUPS.values()) + len(GROUPS)
fig, ax = plt.subplots(figsize=(11, rows * 0.32 + 1))
ax.set_xlim(0, 12); ax.set_ylim(0, rows); ax.axis("off")
y = rows
for group, names in GROUPS.items():
    y -= 1
    ax.text(0, y + .25, group, fontweight="bold", fontsize=11, va="center")
    for name in names:
        y -= 1
        try:
            cols = get(name, 10)
        except Exception:
            cols = ["#dddddd"]
        ax.text(0, y + .45, name, fontsize=9, va="center", ha="left")
        for i, c in enumerate(cols):
            ax.add_patch(Rectangle((3.2 + i * 0.72, y + .12), 0.7, 0.72, color=c))
fig.suptitle("chart_cookbook — palette reference (palettable · pypalettes · matplotlib · Bokeh)",
             fontsize=12, fontweight="bold", y=.995)
plt.tight_layout(rect=[0, 0, 1, .99])
plt.savefig(os.path.join(os.path.dirname(__file__), "..", "figures", "palette_reference.png"), dpi=130)
print("wrote figures/palette_reference.png with", rows, "rows")
