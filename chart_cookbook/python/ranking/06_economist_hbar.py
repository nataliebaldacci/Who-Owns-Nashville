"""Horizontal barplot in The Economist "Escape artists" style. Blue bars, value
labels placed inside (white) or outside (blue, path-effect stroke) depending on
bar length, top x-axis ticks, light grid, and the signature red top line +
rectangle with a title/subtitle/source stack. Davidson data: the largest
corporate operators by parcels (real owner_leaderboard.json)."""
import matplotlib; matplotlib.use("Agg")
import os, json
import matplotlib.pyplot as plt
from matplotlib import lines, patches
from matplotlib.patheffects import withStroke

BLUE = "#076fa2"
RED = "#E3120B"
GREY = "#A8BAC4"

ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
rows = json.load(open(os.path.join(ROOT, "owner_leaderboard.json")))["rows"]
rows = sorted(rows, key=lambda r: r["n"], reverse=True)[:12][::-1]
names = [r["nm"] for r in rows]
counts = [r["n"] for r in rows]

try:  # the Economist uses Econ Sans Cnd; fall back gracefully offline
    from pyfonts import load_font
    FONT = load_font("https://github.com/googlefonts/RobotoCondensed/blob/main/fonts/ttf/RobotoCondensed-Regular.ttf?raw=true")
    BOLD = load_font("https://github.com/googlefonts/RobotoCondensed/blob/main/fonts/ttf/RobotoCondensed-Bold.ttf?raw=true")
except Exception:
    FONT = BOLD = None

fig, ax = plt.subplots(figsize=(9, 10))
y = range(len(names))
ax.barh(y, counts, height=0.55, align="edge", color=BLUE)

# vertical gridlines only, behind the bars, at rounded ticks
step = 300
xmax = (max(counts)//step + 1) * step
ax.xaxis.set_ticks(range(0, xmax + 1, step))
ax.xaxis.set_tick_params(labelbottom=False, labeltop=True, length=0)
ax.set_xlim(0, xmax)
ax.set_ylim(0, len(names))
ax.grid(axis="x", color=GREY, lw=1.2)
ax.set_axisbelow(True)
ax.set_yticks([])
for spine in ["left", "right", "top"]:
    ax.spines[spine].set_visible(False)
ax.spines["bottom"].set_lw(1.2)

# operator names + value labels, inside or outside the bar
INSIDE = xmax * 0.18  # short bars get the label outside
pe = [withStroke(linewidth=6, foreground="white")]
for i, (name, count) in enumerate(zip(names, counts)):
    if count >= INSIDE:
        ax.text(count - xmax*0.01, i + 0.55/2, f"{count:,}", color="white",
                ha="right", va="center", fontsize=13,
                fontproperties=BOLD)
    else:
        ax.text(count + xmax*0.01, i + 0.55/2, f"{count:,}", color=BLUE,
                ha="left", va="center", fontsize=13, path_effects=pe,
                fontproperties=BOLD)
    ax.text(0, i + 0.55 + 0.06, name, color="black", ha="left", va="bottom",
            fontsize=13, fontproperties=FONT)

# red top line + rectangle, title, subtitle, source
fig.add_artist(lines.Line2D([0.05, 0.05], [0.06, 0.94], color=RED, lw=1.6))
fig.add_artist(patches.Rectangle((0.05, 0.94), 0.10, 0.03, color=RED,
                                 transform=fig.transFigure, clip_on=False))
fig.text(0.05, 0.975, "Concentration by the parcel",
         fontsize=22, fontweight="bold", fontproperties=BOLD, va="top")
fig.text(0.05, 0.935,
         "Davidson County single-family holdings, largest corporate operators, parcels owned",
         fontsize=13, fontproperties=FONT, va="top")
fig.text(0.05, 0.02,
         "Source: Who Owns Nashville, assembled from Davidson County parcel and "
         "assessor records\nWho Owns Nashville",
         color="#5a5a5a", fontsize=10, fontproperties=FONT)

plt.subplots_adjust(left=0.05, right=0.97, top=0.90, bottom=0.09)
plt.savefig(os.path.join(os.path.dirname(__file__), "06_economist_hbar.png"), dpi=150)
print("wrote 06_economist_hbar.png")
