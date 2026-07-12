"""Annotated bubble map (eclipse-map style, Joseph Barbier). Davidson county
outline + one bubble per block group, colored by institutional rate and sized by
count, with a highlight_text title, an arrow + ellipse calling out the highest-
concentration cluster, and path-effect labels."""
import matplotlib; matplotlib.use("Agg")
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import Ellipse, FancyArrowPatch
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize
import geopandas as gpd
from highlight_text import fig_text

ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
bg = gpd.read_file(os.path.join(ROOT, "institutional_by_blockgroup.geojson")).to_crs(4326)
outline = gpd.read_file(os.path.join(ROOT, "Davidson_County_Boundary.geojson")).to_crs(4326)
cent = bg.copy(); cent["geometry"] = bg.geometry.centroid
cent["lon"] = cent.geometry.x; cent["lat"] = cent.geometry.y
norm = Normalize(vmin=cent["rate"].min(), vmax=cent["rate"].quantile(0.97))
sm = ScalarMappable(norm=norm, cmap=plt.get_cmap("plasma"))
cent["color"] = cent["rate"].apply(sm.to_rgba)

fig, ax = plt.subplots(figsize=(9, 9)); ax.axis("off")
outline.plot(ax=ax, edgecolor="#1c458c", color="#fffcf2", linewidth=0.8)
ax.scatter(cent["lon"], cent["lat"], c=cent["color"], s=cent["inst"].clip(1)*3,
           edgecolor="black", linewidth=0.2, alpha=0.9)

# highlight the single highest-concentration block group
top = cent.loc[cent["rate"].idxmax()]
ax.scatter([top["lon"]], [top["lat"]], color="white", edgecolor="black", s=60, zorder=10)
ax.add_patch(Ellipse((top["lon"], top["lat"]), width=0.05, height=0.04, edgecolor="black", fill=False, lw=1.6))
fig.patches.append(FancyArrowPatch((0.62, 0.30), (0.74, 0.42),
    connectionstyle="arc3,rad=-.4", transform=fig.transFigure,
    arrowstyle="Simple, tail_width=0.5, head_width=4, head_length=8", color="k"))
stroke = [pe.Stroke(linewidth=0.8, foreground="black"), pe.Normal()]
fig_text(0.30, 0.24, "<Highest institutional concentration>", ha="center", fontsize=11,
         highlight_textprops=[{"weight": "bold"}])

fig_text(0.10, 0.90,
    "Corporate ownership clusters in <southeast Davidson>\n"
    "<Each dot is a block group, colored by institutional rate: the brighter, the higher.>",
    ha="left", va="center", fontsize=15,
    highlight_textprops=[{"color": "#d7263d", "weight": "bold"},
                         {"color": "grey", "fontsize": 10}])
fig.colorbar(sm, ax=ax, shrink=0.4, label="Institutional rate (%)")
plt.savefig("map/38_annotated_bubble_map.png".split("/")[-1], dpi=150, bbox_inches="tight")
print("wrote 38_annotated_bubble_map.png")
