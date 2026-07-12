"""Interval chart with hbar (Bokeh docs "intervals" example). Each row is drawn
as a horizontal bar spanning a min-to-max range with left/right, so the chart
reads as a set of intervals rather than magnitudes. Real data: the span of
acquisition activity for the largest Davidson owner entities — from their first
to their most recent recorded acquisition year, with a dot at the busiest year."""
import os, sys, json, collections
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure
sys.path.insert(0, os.path.dirname(__file__))
from _shared import write

ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
props = [f["properties"] for f in
         json.load(open(os.path.join(ROOT, "Davidson_Active_Corporate_SFR_Detail.geojson")))["features"]]

owners = collections.defaultdict(collections.Counter)
for p in props:
    a = str(p.get("acq", ""))[:4]
    if a.isdigit() and 2010 <= int(a) <= 2025:
        owners[p.get("owner", "?")][int(a)] += 1

top = sorted(owners, key=lambda o: -sum(owners[o].values()))[:16]
names, first, last, peak, tot = [], [], [], [], []
seen = collections.Counter()
for o in top:
    yrs = owners[o]
    nm = o.title()[:26]
    seen[nm] += 1
    if seen[nm] > 1:
        nm = f"{nm} ({seen[nm]})"   # keep y-axis factors unique
    names.append(nm)
    first.append(min(yrs)); last.append(max(yrs))
    peak.append(max(yrs, key=lambda y: yrs[y])); tot.append(sum(yrs.values()))
# order rows by first-acquisition year (earliest at top)
order = sorted(range(len(names)), key=lambda i: (first[i], -tot[i]))
names = [names[i] for i in order]
src = ColumnDataSource(dict(name=names,
    first=[first[i] for i in order], last=[last[i] for i in order],
    peak=[peak[i] for i in order], tot=[tot[i] for i in order]))

p = figure(y_range=names, x_range=(2011, 2026), width=760, height=560, toolbar_location=None,
           title="When each corporate owner was active (first → last acquisition year)")
p.hbar(y="name", left="first", right="last", height=0.5, source=src,
       color="#4fa0bd", line_color="#1c458c")
p.scatter(x="peak", y="name", size=9, source=src, color="#d7263d",
          legend_label="busiest year")
p.add_tools(HoverTool(tooltips=[("owner", "@name"), ("active", "@first–@last"),
                                ("busiest", "@peak"), ("parcels", "@tot")]))
p.ygrid.grid_line_color = None
p.xaxis.axis_label = "acquisition year"
p.legend.location = "bottom_right"
p.outline_line_color = None

write(p, os.path.join(os.path.dirname(__file__), "b21_intervals_hbar.html"),
      "Interval chart — owner activity spans")
