"""Crossfilter (demo.bokeh.org/crossfilter, standalone). Four Select widgets let
you remap the scatter's X, Y, bubble Size and Color to any variable, so you can
explore every pairwise relationship in the data interactively. The official demo
is a Bokeh server app; this is a self-contained HTML version driven by CustomJS
(no server). Real data: Davidson County block groups (institutional rate,
poverty, Black share, income, value, parcel counts)."""
import os, sys
import geopandas as gpd
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, Select, CustomJS
from bokeh.palettes import Viridis256
from bokeh.plotting import figure
sys.path.insert(0, os.path.dirname(__file__))
from _shared import write

ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
bg = gpd.read_file(os.path.join(ROOT, "institutional_by_blockgroup.geojson"))

# friendly label -> raw column, all numeric block-group variables
FIELDS = {
    "Institutional rate (%)": "rate", "Poverty rate (%)": "pov",
    "Black population (%)": "blk", "Median income ($)": "inc",
    "Total assessed value ($)": "val", "Residential parcels": "res",
    "Institutional parcels": "inst",
}
cols = {label: bg[c].fillna(0).astype(float).tolist() for label, c in FIELDS.items()}
labels = list(FIELDS)
xg, yg, sg, cg = "Poverty rate (%)", "Institutional rate (%)", "Institutional parcels", "Median income ($)"


def norm(a):
    lo, hi = min(a), max(a)
    return [(v - lo) / (hi - lo) if hi > lo else 0.5 for v in a]


pal = list(Viridis256)
sz = [6 + t * 24 for t in norm(cols[sg])]
col = [pal[min(len(pal) - 1, int(t * (len(pal) - 1)))] for t in norm(cols[cg])]
source = ColumnDataSource(dict(x=cols[xg], y=cols[yg], sz=sz, col=col))

p = figure(width=640, height=560, tools="pan,wheel_zoom,box_zoom,reset,save",
           x_axis_label=xg, y_axis_label=yg, background_fill_color="#fafafa",
           title="Crossfilter — pick any variable for each axis")
p.scatter("x", "y", size="sz", fill_color="col", line_color="#333333",
          fill_alpha=0.65, source=source)

xs = Select(title="X Axis", value=xg, options=labels)
ys = Select(title="Y Axis", value=yg, options=labels)
ss = Select(title="Size", value=sg, options=labels)
cs = Select(title="Color", value=cg, options=labels)

cb = CustomJS(args=dict(source=source, cols=cols, pal=pal,
                        xs=xs, ys=ys, ss=ss, cs=cs,
                        xaxis=p.xaxis[0], yaxis=p.yaxis[0]), code="""
    function norm(a){ const lo=Math.min(...a), hi=Math.max(...a);
        return a.map(v => hi>lo ? (v-lo)/(hi-lo) : 0.5); }
    const sv = norm(cols[ss.value]);
    const cv = norm(cols[cs.value]);
    source.data = {
        x: cols[xs.value],
        y: cols[ys.value],
        sz: sv.map(t => 6 + t*24),
        col: cv.map(t => pal[Math.min(pal.length-1, Math.floor(t*(pal.length-1)))]),
    };
    xaxis.axis_label = xs.value;
    yaxis.axis_label = ys.value;
    source.change.emit();
""")
for w in (xs, ys, ss, cs):
    w.js_on_change("value", cb)

layout = row(column(xs, ys, ss, cs), p)
write(layout, os.path.join(os.path.dirname(__file__), "b16_crossfilter.html"),
      "Crossfilter — Davidson block groups")
