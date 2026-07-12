"""Draw a map straight from a GeoJSON with GeoPandas + GeoPlot (python-graph-
gallery "polyplot" style). Loads a Davidson boundary layer into a GeoDataFrame
and draws the polygons with geoplot.polyplot on an AlbersEqualArea projection.
Falls back to plain geopandas .plot() if geoplot/cartopy are unavailable."""
import matplotlib; matplotlib.use("Agg")
import os
import matplotlib.pyplot as plt
import geopandas as gpd

ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
# any polygon layer works; community planning areas give a clean county outline
data = gpd.read_file(os.path.join(ROOT, "Davidson_Community_Planning_Areas.geojson")).to_crs(4326)
print(type(data), "->", len(data), "regions")

try:
    import geoplot
    import geoplot.crs as gcrs
    ax = geoplot.polyplot(
        data,
        projection=gcrs.AlbersEqualArea(),
        edgecolor="darkgrey",
        facecolor="lightgrey",
        linewidth=0.3,
        figsize=(12, 8),
    )
    ax.set_title("Davidson County community planning areas", fontsize=15, loc="left")
    fig = ax.get_figure()
except Exception as e:  # geoplot/cartopy missing -> plain geopandas
    print("geoplot unavailable (%s); using geopandas .plot()" % e)
    fig, ax = plt.subplots(figsize=(12, 8))
    data.plot(ax=ax, edgecolor="darkgrey", facecolor="lightgrey", linewidth=0.3)
    ax.set_title("Davidson County community planning areas", fontsize=15, loc="left")
    ax.axis("off")

plt.savefig(os.path.join(os.path.dirname(__file__), "40_geoplot_polyplot.png"),
            dpi=150, bbox_inches="tight")
print("wrote 40_geoplot_polyplot.png")
