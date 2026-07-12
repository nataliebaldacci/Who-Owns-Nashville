"""Interactive choropleth with Plotly Express (python-graph-gallery style).
Loads a Davidson GeoJSON, colors each census tract by institutional ownership
rate with px.choropleth_map, and writes a self-contained interactive HTML with
hover readouts. Mirrors the plotly.express.choropleth idiom (geojson + locations
+ color) adapted from US counties to Davidson tracts."""
import os, json
import geopandas as gpd
import plotly.express as px

ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
geo = gpd.read_file(os.path.join(ROOT, "Davidson_Institutional_Pct_by_Tract.geojson")).to_crs(4326)
col = next((c for c in ["pct_institutional", "institutional_pct", "rate", "pct", "value"]
            if c in geo.columns), geo.select_dtypes("number").columns[-1])
idc = next((c for c in ["GEOID", "geoid", "tract", "id", "NAME"] if c in geo.columns), None)
if idc is None:
    geo = geo.reset_index().rename(columns={"index": "id"}); idc = "id"
geo[idc] = geo[idc].astype(str)
geo = geo[geo[col].notna()].copy()

gj = json.loads(geo.to_json())
fig = px.choropleth(
    geo, geojson=gj, locations=idc, featureidkey="properties." + idc,
    color=col, color_continuous_scale="YlOrBr",
    range_color=(0, geo[col].quantile(0.97)),
    labels={col: "Institutional rate"},
)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(
    margin={"r": 0, "t": 40, "l": 0, "b": 0},
    title="Institutional ownership rate by tract — Davidson County",
    coloraxis_colorbar=dict(thicknessmode="pixels", thickness=12,
                            lenmode="pixels", len=200, yanchor="top", y=0.85,
                            ticks="outside", ticksuffix=" %"),
)
out = os.path.join(os.path.dirname(__file__), "42_plotly_choropleth.html")
fig.write_html(out, include_plotlyjs="inline")
print("wrote 42_plotly_choropleth.html  (column=%s, id=%s, tracts=%d)" % (col, idc, len(geo)))
