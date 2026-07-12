"""Bubble map with Basemap (python-graph-gallery style). Basemap draws the
background (county extent, land fill, coastline-style boundary) and matplotlib
scatters one orange bubble per point, sized by a third variable. Real data:
corporate SFR parcels in Davidson County, bubbles at block-group centroids sized
by parcel count. Falls back to a plain geopandas outline + scatter if Basemap is
unavailable (Basemap is legacy and often not installed)."""
import matplotlib; matplotlib.use("Agg")
import os
import matplotlib.pyplot as plt
import geopandas as gpd

ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
bg = gpd.read_file(os.path.join(ROOT, "institutional_by_blockgroup.geojson")).to_crs(4326)
cent = bg.copy(); cent["geometry"] = bg.geometry.centroid
cent = cent[cent["inst"].fillna(0) > 0]
lon, lat, n = cent.geometry.x.values, cent.geometry.y.values, cent["inst"].clip(1).values

# county bounding box with a small margin
minx, miny, maxx, maxy = bg.total_bounds
pad = 0.02

fig = plt.figure(figsize=(9, 10))
try:
    from mpl_toolkits.basemap import Basemap
    m = Basemap(llcrnrlon=minx - pad, llcrnrlat=miny - pad,
                urcrnrlon=maxx + pad, urcrnrlat=maxy + pad,
                resolution="i", projection="cyl")
    m.drawmapboundary(fill_color="#A6CAE0", linewidth=0)
    m.fillcontinents(color="#e8e6df", alpha=0.9, lake_color="#A6CAE0")
    m.drawcoastlines(linewidth=0.2, color="white")
    m.drawcounties(linewidth=0.4, color="#8a8a8a")
    x, y = m(lon, lat)
    m.scatter(x, y, alpha=0.5, s=n / 2, c="#f0af1e", linewidth=0.6, edgecolor="black", zorder=5)
    ax = plt.gca()
except Exception as e:
    print("Basemap unavailable (%s); using geopandas outline + scatter" % e)
    ax = plt.gca()
    bg.dissolve().plot(ax=ax, color="#e8e6df", edgecolor="#8a8a8a", linewidth=0.4)
    ax.scatter(lon, lat, alpha=0.5, s=n / 2, c="#f0af1e", linewidth=0.6, edgecolor="black")
    ax.set_facecolor("#A6CAE0")

ax.set_title("Corporate SFR concentration — Davidson County\n"
             "bubble size = institutional parcels per block group",
             fontsize=14, loc="left")
ax.axis("off")
plt.savefig(os.path.join(os.path.dirname(__file__), "43_basemap_bubble.png"),
            dpi=150, bbox_inches="tight")
print("wrote 43_basemap_bubble.png  (%d bubbles)" % len(cent))
