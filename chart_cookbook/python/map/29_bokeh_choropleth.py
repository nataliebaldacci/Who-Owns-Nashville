"""Bokeh interactive choropleth — MAP. Adapts the Bokeh county-unemployment
example (LogColorMapper + HoverTool) to Davidson tracts / institutional %.
Self-contained HTML via INLINE resources. Writes 29_bokeh_choropleth.html."""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import geopandas as gpd
from bokeh.models import LinearColorMapper, ColorBar, HoverTool
from bokeh.plotting import figure, output_file, save
from bokeh.resources import INLINE
from styles.palettes import get
ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")

gdf = gpd.read_file(os.path.join(ROOT, "Davidson_Institutional_Pct_by_Tract.geojson")).to_crs(4326)
palette = tuple(get("jchs_orange")) if False else tuple(get("YlOrBr", 6))

def coords(geom, kind):
    # return list-of-rings for (multi)polygons; xs()->lon, ys()->lat
    polys = geom.geoms if geom.geom_type == "MultiPolygon" else [geom]
    out = []
    for p in polys:
        out.append(list(p.exterior.coords.xy[0 if kind == "x" else 1]))
    return out

xs, ys, names, rates = [], [], [], []
for _, r in gdf.iterrows():
    g = r.geometry
    if g is None: continue
    for ring_x, ring_y in zip(coords(g, "x"), coords(g, "y")):
        xs.append(list(ring_x)); ys.append(list(ring_y))
        names.append(r["TRACTCE"]); rates.append(float(r["pct_institutional"] or 0))

mapper = LinearColorMapper(palette=palette, low=min(rates), high=max(rates))
data = dict(x=xs, y=ys, name=names, rate=rates)
TOOLS = "pan,wheel_zoom,reset,hover,save"
p = figure(title="Davidson County — Institutional Ownership by Tract (%)", tools=TOOLS,
           x_axis_location=None, y_axis_location=None, width=760, height=780,
           match_aspect=True,
           tooltips=[("Tract", "@name"), ("Institutional", "@rate%")])
p.grid.grid_line_color = None
p.hover.point_policy = "follow_mouse"
p.patches("x", "y", source=data,
          fill_color={"field": "rate", "transform": mapper},
          fill_alpha=0.8, line_color="white", line_width=0.4)
p.add_layout(ColorBar(color_mapper=mapper, title="Institutional %"), "right")
output_file("29_bokeh_choropleth.html", title="Davidson Institutional Choropleth")
save(p, resources=INLINE)
print("wrote 29_bokeh_choropleth.html")
