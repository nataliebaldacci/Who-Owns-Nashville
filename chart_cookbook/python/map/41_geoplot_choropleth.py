"""Choropleth map with GeoPandas + GeoPlot (python-graph-gallery style). Loads a
Davidson GeoJSON, uses a mapclassify Quantiles(k) binning scheme, and draws the
choropleth with gplt.choropleth on an AlbersEqualArea projection (inferno_r).
Real data: institutional ownership rate by census tract. Falls back to a plain
geopandas quantile choropleth if geoplot/cartopy are unavailable."""
import matplotlib; matplotlib.use("Agg")
import os
import matplotlib.pyplot as plt
import geopandas as gpd
import mapclassify as mc

ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
geo = gpd.read_file(os.path.join(ROOT, "Davidson_Institutional_Pct_by_Tract.geojson")).to_crs(4326)
# find the numeric rate column
col = next((c for c in ["institutional_pct", "inst_pct", "pct", "rate", "value"]
            if c in geo.columns), None)
if col is None:
    col = geo.select_dtypes("number").columns[-1]
geo = geo[geo[col].notna()].copy()
k = min(10, geo[col].nunique())
scheme = mc.Quantiles(geo[col], k=k)

try:
    import geoplot as gplt
    import geoplot.crs as gcrs
    ax = gplt.choropleth(
        geo, projection=gcrs.AlbersEqualArea(),
        hue=col, scheme=scheme, cmap="inferno_r",
        linewidth=0.1, edgecolor="black", legend=True, figsize=(12, 9),
    )
    ax.set_title("Institutional ownership rate by tract — Davidson County",
                 fontsize=15, loc="left")
    fig = ax.get_figure()
except Exception as e:
    print("geoplot unavailable (%s); using geopandas quantile plot" % e)
    fig, ax = plt.subplots(figsize=(12, 9)); ax.axis("off")
    geo.plot(column=col, scheme="Quantiles", k=k, cmap="inferno_r",
             linewidth=0.1, edgecolor="black", legend=True, ax=ax)
    ax.set_title("Institutional ownership rate by tract — Davidson County",
                 fontsize=15, loc="left")

plt.savefig(os.path.join(os.path.dirname(__file__), "41_geoplot_choropleth.png"),
            dpi=150, bbox_inches="tight")
print("wrote 41_geoplot_choropleth.png  (column=%s, k=%d)" % (col, k))
