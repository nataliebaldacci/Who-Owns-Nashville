"""Interactive filtered scatter with sliders (demo.bokeh.org/movies, standalone).
Sliders and a Select filter a large point cloud live; the scatter and its title
count update via CustomJS as you drag. The official movies demo is a Bokeh
server app; this is a self-contained HTML version (no server). Real data:
Davidson County corporate SFR parcels — living area vs year built, filterable by
minimum beds, minimum living area, acquisition year, and property type, with a
hover tooltip showing the address and owner."""
import os, sys, json
import numpy as np
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, Slider, Select, CustomJS, HoverTool, Div
from bokeh.plotting import figure
sys.path.insert(0, os.path.dirname(__file__))
from _shared import write

ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
props = [f["properties"] for f in
         json.load(open(os.path.join(ROOT, "Davidson_Active_Corporate_SFR_Detail.geojson")))["features"]]

rows = []
for p in props:
    sq, yb, bd, a, pt = (str(p.get("sqft", "")), str(p.get("ybuilt", "")),
                         str(p.get("beds", "")), str(p.get("acq", ""))[:4], p.get("ptype") or "Other")
    if sq.replace(".", "").isdigit() and yb.isdigit() and a.isdigit():
        rows.append(dict(sqft=float(sq), ybuilt=int(yb), beds=int(bd) if bd.isdigit() else 0,
                         acq=int(a), ptype=pt,
                         addr=str(p.get("addr", ""))[:40], owner=str(p.get("owner", ""))[:34]))
rng = np.random.RandomState(1)
if len(rows) > 3000:
    rows = [rows[i] for i in rng.choice(len(rows), 3000, replace=False)]
rows = [r for r in rows if 1900 < r["ybuilt"] <= 2025 and r["sqft"] < 6000]

def col(k): return [r[k] for r in rows]
full = dict(sqft=col("sqft"), ybuilt=col("ybuilt"), beds=col("beds"), acq=col("acq"),
            ptype=col("ptype"), addr=col("addr"), owner=col("owner"))
view = ColumnDataSource(dict(x=full["sqft"], y=col("ybuilt"), addr=full["addr"], owner=full["owner"]))

ptypes = ["All"] + sorted({r["ptype"] for r in rows})
p = figure(width=680, height=560, tools="pan,wheel_zoom,box_zoom,reset,save",
           x_axis_label="Living area (sq ft)", y_axis_label="Year built",
           background_fill_color="#fafafa", title="Corporate parcels — drag the sliders to filter")
p.scatter("x", "y", source=view, size=6, color="#1c458c", alpha=0.5)
p.add_tools(HoverTool(tooltips=[("Address", "@addr"), ("Owner", "@owner")]))

s_beds = Slider(title="Minimum beds", start=0, end=6, value=0, step=1)
s_sqft = Slider(title="Minimum living area (sq ft)", start=0, end=4000, value=0, step=100)
s_year = Slider(title="Acquired since (year)", start=2012, end=2025, value=2012, step=1)
sel_pt = Select(title="Property type", value="All", options=ptypes)
count = Div(text="")

cb = CustomJS(args=dict(view=view, full=full, count=count,
                        s_beds=s_beds, s_sqft=s_sqft, s_year=s_year, sel_pt=sel_pt), code="""
    const n = full.sqft.length;
    const x=[], y=[], addr=[], owner=[];
    for (let i=0; i<n; i++) {
        if (full.beds[i] < s_beds.value) continue;
        if (full.sqft[i] < s_sqft.value) continue;
        if (full.acq[i] < s_year.value) continue;
        if (sel_pt.value !== "All" && full.ptype[i] !== sel_pt.value) continue;
        x.push(full.sqft[i]); y.push(full.ybuilt[i]);
        addr.push(full.addr[i]); owner.push(full.owner[i]);
    }
    view.data = {x, y, addr, owner};
    view.change.emit();
    count.text = "<b>" + x.length + "</b> parcels match";
""")
for w in (s_beds, s_sqft, s_year, sel_pt):
    w.js_on_change("value", cb)

layout = row(column(sel_pt, s_beds, s_sqft, s_year, count), p)
write(layout, os.path.join(os.path.dirname(__file__), "b17_movies_filter.html"),
      "Filtered scatter with sliders — Davidson corporate parcels")
