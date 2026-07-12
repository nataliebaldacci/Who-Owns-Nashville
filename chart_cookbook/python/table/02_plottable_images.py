"""Publication table with logos, in the plottable "add images in a column" style
(Joseph Barbier / python-graph-gallery). Each operator row carries a circular
badge in an Image column via plot_fn=circled_image. Because logo files ship with
no repo, the script first renders a simple colored initial-badge PNG per operator
into ./badges/, then feeds those filenames to plottable. Real owner_leaderboard
data; swap the badge folder for real company logos to publish."""
import matplotlib; matplotlib.use("Agg")
import os, json
import matplotlib.pyplot as plt
import pandas as pd
from plottable import ColumnDefinition, Table
from plottable.plots import circled_image

HERE = os.path.dirname(__file__)
ROOT = os.path.join(HERE, "..", "..", "..")
BADGES = os.path.join(HERE, "badges")
os.makedirs(BADGES, exist_ok=True)

# stable per-operator brand colors (matches the cookbook qualitative set)
COLORS = ["#e6194b", "#2166ac", "#1a9850", "#911eb4", "#16a085", "#cf307a",
          "#f58231", "#0b6e4f", "#8d6e63", "#c2185b", "#00897b", "#5d4037"]

rows = json.load(open(os.path.join(ROOT, "owner_leaderboard.json")))["rows"][:8]

def initials(name):
    parts = [p for p in name.replace("/", " ").split() if p[:1].isalpha()]
    return "".join(p[0] for p in parts[:2]).upper() or name[:2].upper()

def make_badge(name, color, path):
    """Render a flat circular initial-badge PNG for a company."""
    fig, ax = plt.subplots(figsize=(1, 1), dpi=120)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.add_patch(plt.Circle((0.5, 0.5), 0.46, color=color))
    ax.text(0.5, 0.5, initials(name), ha="center", va="center",
            color="white", fontsize=22, fontweight="bold")
    fig.savefig(path, transparent=True, bbox_inches="tight", pad_inches=0)
    plt.close(fig)

recs = []
for i, r in enumerate(rows):
    fname = os.path.join(BADGES, f"op{i}.png")
    make_badge(r["nm"], COLORS[i % len(COLORS)], fname)
    recs.append({
        "Logo": fname,
        "Operator": r["nm"],
        "Parcels": r["n"],
        "Units": r.get("du", 0),
        "Value $M": round(r.get("val", 0) / 1e6),
    })
df = pd.DataFrame(recs).set_index("Operator")

col_defs = [
    ColumnDefinition(name="Logo", title="", textprops={"ha": "center"},
                     width=0.6, plot_fn=circled_image),
    ColumnDefinition(name="Parcels", textprops={"ha": "center"}, width=0.7),
    ColumnDefinition(name="Units", textprops={"ha": "center"}, width=0.7),
    ColumnDefinition(name="Value $M", textprops={"ha": "center"}, width=0.8),
]

plt.rcParams["font.family"] = ["DejaVu Sans"]
fig, ax = plt.subplots(figsize=(9, 6))
Table(df, column_definitions=col_defs, ax=ax,
      textprops={"fontsize": 13, "ha": "left"},
      row_dividers=True, footer_divider=True,
      row_divider_kw={"linewidth": 1, "linestyle": (0, (1, 5))})
fig.text(0.06, 0.94, "DAVIDSON COUNTY — TOP CORPORATE OPERATORS",
         fontsize=16, fontweight="bold")
fig.text(0.06, 0.905, "Badge = operator initials; swap ./badges for real logos",
         fontsize=10, color="#5a5a5a")
plt.savefig(os.path.join(HERE, "02_plottable_images.png"), dpi=150, bbox_inches="tight")
print("wrote 02_plottable_images.png")
