"""Categorical bubble map with Basemap (python-graph-gallery surf-tweets style).
Basemap draws the background; matplotlib scatters one bubble per block group,
sized by institutional parcel count and colored by category (the dominant
operator) via pd.factorize + a Set1 colormap, with a source/copyright text
block. Real Davidson data. Falls back to a plain geopandas outline + scatter if
Basemap is unavailable (Basemap is legacy and often not installed)."""
import matplotlib; matplotlib.use("Agg")
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
import geopandas as gpd
bg = gpd.read_file(os.path.join(ROOT, "institutional_by_blockgroup.geojson")).to_crs(4326)
cent = bg.copy(); cent["geometry"] = bg.geometry.centroid
cent = cent[(cent["inst"].fillna(0) > 0) & (cent["top"].fillna("").str.len() > 0)].copy()

# collapse dominant operator to the top categories + Other, then factorize
KEEP = ["Amherst Residential", "Progress Residential", "American Homes 4 Rent",
        "Tricon Residential", "Starwood"]
cent["cat"] = np.where(cent["top"].isin(KEEP), cent["top"], "Other")
cats = KEEP + ["Other"]
cent["cat"] = pd.Categorical(cent["cat"], categories=cats, ordered=True)
codes = cent["cat"].cat.codes.values
lon, lat, n = cent.geometry.x.values, cent.geometry.y.values, cent["inst"].clip(1).values
cmap = plt.get_cmap("Set1", len(cats))

minx, miny, maxx, maxy = bg.total_bounds; pad = 0.02
plt.rcParams["figure.figsize"] = 11, 11
fig = plt.figure()
try:
    from mpl_toolkits.basemap import Basemap
    m = Basemap(llcrnrlon=minx - pad, llcrnrlat=miny - pad,
                urcrnrlon=maxx + pad, urcrnrlat=maxy + pad, resolution="i", projection="cyl")
    m.drawmapboundary(fill_color="#A6CAE0", linewidth=0)
    m.fillcontinents(color="#e8e6df", alpha=0.9, lake_color="#A6CAE0")
    m.drawcoastlines(linewidth=0.2, color="white")
    m.drawcounties(linewidth=0.4, color="#8a8a8a")
    x, y = m(lon, lat)
    sc = m.scatter(x, y, s=n / 2, alpha=0.55, c=codes, cmap=cmap, vmin=0, vmax=len(cats) - 1,
                   edgecolor="black", linewidth=0.4, zorder=5)
    ax = plt.gca()
except Exception as e:
    print("Basemap unavailable (%s); using geopandas outline + scatter" % e)
    ax = plt.gca()
    bg.dissolve().plot(ax=ax, color="#e8e6df", edgecolor="#8a8a8a", linewidth=0.4)
    ax.scatter(lon, lat, s=n / 2, alpha=0.55, c=codes, cmap=cmap, vmin=0, vmax=len(cats) - 1,
               edgecolor="black", linewidth=0.4)
    ax.set_facecolor("#A6CAE0")

handles = [Line2D([0], [0], marker="o", linestyle="", markersize=9,
                  markerfacecolor=cmap(i), markeredgecolor="black", label=c)
           for i, c in enumerate(cats)]
ax.legend(handles=handles, title="Dominant operator", loc="lower left",
          fontsize=9, title_fontsize=10, framealpha=0.9)
ax.axis("off")
ax.set_title("Where corporate operators dominate — Davidson County block groups\n"
             "bubble size = institutional parcels, color = dominant operator",
             fontsize=14, loc="left")
fig.text(0.12, 0.06, "Data: Who Owns Nashville, Davidson County parcel records\n"
         "Plot realized with Python and the Basemap library",
         ha="left", va="bottom", size=9, color="#555555")
plt.savefig(os.path.join(os.path.dirname(__file__), "45_basemap_bubble_categorical.png"),
            dpi=150, bbox_inches="tight")
print("wrote 45_basemap_bubble_categorical.png  (%d bubbles, %d categories)" % (len(cent), len(cats)))
