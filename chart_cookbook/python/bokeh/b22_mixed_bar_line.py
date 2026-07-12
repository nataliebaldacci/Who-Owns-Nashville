"""Combined bar + line chart over nested categorical factors (Bokeh docs "mixed"
example). Vbars sit on nested (era, decade) factors while a line rides the
top-level (era) summary, mixing fine and coarse categories on one x-axis. Real
data: Davidson corporate SFR acquisitions bucketed by build era and build
decade — bars are parcels per decade, the line is the per-era total."""
import os, sys, json, collections
from bokeh.models import FactorRange, ColumnDataSource
from bokeh.plotting import figure
sys.path.insert(0, os.path.dirname(__file__))
from _shared import write

ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
props = [f["properties"] for f in
         json.load(open(os.path.join(ROOT, "Davidson_Active_Corporate_SFR_Detail.geojson")))["features"]]

def era(d): return "Older (pre-1980)" if d < 1980 else ("Mid (1980-1999)" if d < 2000 else "Newer (2000+)")
DEC = {"Older (pre-1980)": ["1940s", "1950s", "1960s", "1970s"],
       "Mid (1980-1999)": ["1980s", "1990s"],
       "Newer (2000+)": ["2000s", "2010s", "2020s"]}

counts = collections.Counter()
for p in props:
    yb = str(p.get("ybuilt", ""))
    if yb.isdigit() and 1940 <= int(yb) <= 2029:
        counts[(era(int(yb)), f"{int(yb)//10*10}s")] += 1

eras = ["Older (pre-1980)", "Mid (1980-1999)", "Newer (2000+)"]
factors = [(e, d) for e in eras for d in DEC[e]]
bar_counts = [counts.get((e, d), 0) for (e, d) in factors]
era_totals = [sum(counts.get((e, d), 0) for d in DEC[e]) for e in eras]

from bokeh.palettes import TolPRGn4
fill_color, line_color = TolPRGn4[2:]
p = figure(x_range=FactorRange(*factors), height=480, width=880, tools="",
           background_fill_color="#fafafa", toolbar_location=None,
           title="Corporate SFR holdings by build era and decade (bars = decade, line = era total)")
p.vbar(x=factors, top=bar_counts, width=0.85, fill_color=fill_color, fill_alpha=0.85,
       line_color=line_color, line_width=1.2)
p.line(x=eras, y=era_totals, color=line_color, line_width=3)
p.scatter(x=eras, y=era_totals, size=11, line_color=line_color, fill_color="white", line_width=3)
p.y_range.start = 0
p.x_range.range_padding = 0.08
p.xaxis.major_label_orientation = 1
p.xgrid.grid_line_color = None
p.yaxis.axis_label = "parcels"

write(p, os.path.join(os.path.dirname(__file__), "b22_mixed_bar_line.html"),
      "Mixed bar + line — holdings by era and decade")
