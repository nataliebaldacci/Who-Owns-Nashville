"""Gapminder-style animated bubble with a year Slider (demo.bokeh.org/gapminder,
standalone). Bubbles move as you drag the slider through the years. The official
demo is a Bokeh server app; this is a self-contained HTML version driven by
CustomJS. Real data: for each of the largest Davidson owner entities and each
year, x = cumulative parcels held (log), y = share of those holdings built in
2000 or later, bubble size = parcels acquired that year. Watch operators
accumulate (move right) and tilt toward newer stock (move up) over time."""
import os, sys, json, collections
import numpy as np
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider, CustomJS, Label
from bokeh.palettes import Category10_10
from bokeh.plotting import figure
sys.path.insert(0, os.path.dirname(__file__))
from _shared import write

ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
props = [f["properties"] for f in
         json.load(open(os.path.join(ROOT, "Davidson_Active_Corporate_SFR_Detail.geojson")))["features"]]

YEARS = list(range(2013, 2026))
# per owner: list of (acq_year, is_new)
owners = collections.defaultdict(list)
for p in props:
    a, yb = str(p.get("acq", ""))[:4], str(p.get("ybuilt", ""))
    if a.isdigit() and yb.isdigit() and 2010 <= int(a) <= 2025:
        owners[p.get("owner", "?")].append((int(a), int(yb) >= 2000))
top = sorted(owners, key=lambda o: -len(owners[o]))[:10]
colors = list(Category10_10)

# build per-year snapshot: x=cum parcels, y=% new (cumulative), size=that year's acquisitions
snap = {}   # year -> dict(x,y,size,color,name)
for y in YEARS:
    xs, ys, sizes, cols, names = [], [], [], [], []
    for i, o in enumerate(top):
        hist = [h for h in owners[o] if h[0] <= y]
        if not hist:
            continue
        cum = len(hist)
        pct_new = 100 * sum(h[1] for h in hist) / cum
        this_year = sum(1 for h in owners[o] if h[0] == y)
        xs.append(cum); ys.append(pct_new)
        sizes.append(10 + this_year ** 0.5 * 6)
        cols.append(colors[i]); names.append(o.title()[:20])
    snap[str(y)] = dict(x=xs, y=ys, size=sizes, color=cols, name=names)

y0 = str(YEARS[0])
source = ColumnDataSource(snap[y0])

p = figure(width=720, height=560, x_axis_type="log", x_range=(1, 400), y_range=(-5, 105),
           x_axis_label="Cumulative parcels held (log)", y_axis_label="Share of holdings built 2000+ (%)",
           background_fill_color="#fafafa", title="Davidson operators over time (drag the year slider)")
p.scatter("x", "y", size="size", fill_color="color", line_color="#333333", fill_alpha=0.7, source=source)
yr_label = Label(x=20, y=90, text=y0, text_font_size="52px", text_color="#e8e8e8", text_align="left")
p.add_layout(yr_label)

slider = Slider(start=YEARS[0], end=YEARS[-1], value=YEARS[0], step=1, title="Year")
cb = CustomJS(args=dict(source=source, snap=snap, slider=slider, yr_label=yr_label), code="""
    const y = String(slider.value);
    source.data = snap[y];
    source.change.emit();
    yr_label.text = y;
""")
slider.js_on_change("value", cb)

write(column(slider, p), os.path.join(os.path.dirname(__file__), "b19_gapminder.html"),
      "Gapminder bubble — Davidson operators over time")
