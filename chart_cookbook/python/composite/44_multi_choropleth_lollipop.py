"""Multiple choropleth maps with a lollipop plot for the legend (Joseph Barbier
"happiness in Europe" style). Four small block-group choropleths on a dark
background, each a different neighborhood factor with its own two-color gradient,
plus a lollipop panel that shows each factor's min-to-max spread as the legend.
highlight_text titles/annotations and curved FancyArrowPatch arrows finish it.

Real Davidson data: four factors that travel with corporate ownership across
block groups — institutional rate, poverty, Black population share, and the
share of corporate parcels built in 2000 or later (spatial-joined)."""
import matplotlib; matplotlib.use("Agg")
import os, json
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import FancyArrowPatch
import matplotlib.patheffects as path_effects
import pandas as pd
try:
    from highlight_text import ax_text
    HL = True
except Exception:
    HL = False

ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
bg = gpd.read_file(os.path.join(ROOT, "institutional_by_blockgroup.geojson")).to_crs(4326)

# 4th factor: share of corporate parcels built 2000+ per block group (spatial join)
det = json.load(open(os.path.join(ROOT, "Davidson_Active_Corporate_SFR_Detail.geojson")))
pts = gpd.GeoDataFrame.from_features(det["features"], crs=4326)
pts["yb"] = [int(p["ybuilt"]) if str(p.get("ybuilt", "")).isdigit() else np.nan
             for p in [f["properties"] for f in det["features"]]]
pts = pts[pts["yb"].notna()]
j = gpd.sjoin(pts[["yb", "geometry"]], bg[["bg", "geometry"]], how="inner", predicate="within")
newshare = j.groupby("bg")["yb"].apply(lambda s: 100 * (s >= 2000).mean())
bg["newpct"] = bg["bg"].map(newshare)

FACTORS = [
    ("rate",  "institutional rate",   ["#caf0f8", "#0077b6"]),
    ("pov",   "poverty",              ["#fcbf49", "#d62828"]),
    ("blk",   "Black population share",["#c9ada7", "#4a4e69"]),
    ("newpct","corporate stock built 2000+", ["#80ed99", "#38a3a5"]),
]
BG = "#22333b"

def cmap_of(colors):
    return LinearSegmentedColormap.from_list("g", colors, N=256)

def draw_map(col, ax, cmap):
    bg.plot(column=col, cmap=cmap, edgecolor="black", linewidth=0.25, ax=ax,
            missing_kwds={"color": "#3a4a52"})
    ax.axis("off")

fig, axs = plt.subplots(3, 2, figsize=(8.5, 11))
axs = axs.flatten()
fig.set_facecolor(BG)
axs[1].set_facecolor(BG)
layout = [None, None, 0, 1, 2, 3]   # axes 0,1 reserved for title/lollipop
for i, fi in enumerate(layout):
    if fi is None:
        continue
    key, _, colors = FACTORS[fi]
    draw_map(key, axs[i], cmap_of(colors))

# --- lollipop legend in axs[1] ---
def pe(lw=1, fg="black"):
    return [path_effects.Stroke(linewidth=lw, foreground=fg), path_effects.Normal()]

lolli = axs[1]
mins = [bg[k].min() for k, _, _ in FACTORS]
maxs = [np.nanpercentile(bg[k], 99) for k, _, _ in FACTORS]
for i, (k, lab, colors) in enumerate(FACTORS):
    lolli.hlines(i, mins[i], maxs[i], color="white", lw=0.9, zorder=1)
    lolli.scatter(mins[i], i, s=150, color=colors[0], edgecolor="black", lw=0.5, zorder=2)
    lolli.scatter(maxs[i], i, s=150, color=colors[1], edgecolor="black", lw=0.5, zorder=2)
    if HL:
        ax_text(maxs[i] + 3, i, "<" + lab + ">", ax=lolli, va="center", fontsize=8.5,
                fontweight="bold", color=cmap_of(colors)(0.6),
                highlight_textprops=[{"path_effects": pe()}])
    else:
        lolli.text(maxs[i] + 3, i, lab, va="center", fontsize=8.5, color=colors[1])
lolli.spines[["right", "top", "left"]].set_visible(False)
lolli.spines["bottom"].set_color("white")
lolli.tick_params(axis="x", colors="white", labelsize=8)
lolli.set_yticks([]); lolli.set_ylim(-1, 5); lolli.set_xlim(-2, 100)
lolli.set_xlabel("range across block groups (%)", color="white", fontsize=8)
lolli.text(mins[0], 4.4, "min", color="white", fontsize=8)
lolli.text(maxs[0], 4.4, "max", color="white", fontsize=8)

# --- title in axs[0] ---
axs[0].set_axis_off()
title = ("\n<What travels with corporate>\n<ownership in Nashville?>\n"
         "<Four block-group factors. For each map, the darker>\n"
         "<the color, the higher that factor. Corporate holdings>\n"
         "<cluster where poverty and Black population share are high.>")
if HL:
    ax_text(0.0, 0.5, title, ax=axs[0], ha="left", va="center", fontsize=13, color="black",
            highlight_textprops=[{"fontweight": "bold", "color": "white"},
                                 {"fontweight": "bold", "color": "white"},
                                 {"color": "darkgrey", "fontsize": 9},
                                 {"color": "darkgrey", "fontsize": 9},
                                 {"color": "darkgrey", "fontsize": 9}])
else:
    axs[0].text(0.0, 0.5, "What travels with corporate ownership in Nashville?",
                color="white", fontsize=13, fontweight="bold", va="center")

# per-map factor labels
for i, fi in enumerate(layout):
    if fi is None:
        continue
    key, lab, colors = FACTORS[fi]
    axs[i].annotate(lab, (0.5, -0.02), xycoords="axes fraction", ha="center", va="top",
                    fontsize=9, fontweight="bold", color=cmap_of(colors)(0.6),
                    path_effects=pe())

# credit + legend arrows
fig.text(0.06, 0.02, "Design: Who Owns Nashville   Data: Davidson County parcels, ACS block groups",
         color="white", fontsize=7)
def arrow(tail, head, invert=False):
    a = FancyArrowPatch(tail, head, transform=fig.transFigure,
                        connectionstyle="arc3,rad=%s.5" % ("-" if invert else ""),
                        arrowstyle="Simple, tail_width=0.5, head_width=4, head_length=8",
                        color="white")
    fig.patches.append(a)
lolli.set_position([0.56, 0.80, 0.30, 0.11])

plt.savefig(os.path.join(os.path.dirname(__file__), "44_multi_choropleth_lollipop.png"),
            dpi=200, bbox_inches="tight", facecolor=BG)
print("wrote 44_multi_choropleth_lollipop.png  (newpct on %d/%d BGs)"
      % (bg["newpct"].notna().sum(), len(bg)))
