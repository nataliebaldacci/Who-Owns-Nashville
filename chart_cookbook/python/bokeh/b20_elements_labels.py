"""Scatter with hover tooltips and per-point labels (Bokeh docs "elements"
example). Each point carries a text label via LabelSet and a hover tooltip, and
color encodes a third variable through a manual palette bucket. Real data: the
largest Davidson operators — x = average parcel value, y = parcels held, colored
by out-of-state share, labeled with a short operator tag."""
import os, sys, json
from bokeh.models import ColumnDataSource, LabelSet, HoverTool
from bokeh.plotting import figure
sys.path.insert(0, os.path.dirname(__file__))
from _shared import write

ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
rows = json.load(open(os.path.join(ROOT, "owner_leaderboard.json")))["rows"][:22]

palette = ["#053061", "#2166ac", "#4393c3", "#92c5de", "#d1e5f0",
           "#f7f7f7", "#fddbc7", "#f4a582", "#d6604d", "#b2182b", "#67001f"]
def tag(nm):
    return "".join(w[0] for w in nm.replace("/", " ").split()[:3]).upper()

recs = []
for r in rows:
    n = max(r["n"], 1)
    oos = 100 * r.get("oos_n", 0) / n
    recs.append(dict(x=r.get("val", 0) / n / 1000, y=n, name=r["nm"], tag=tag(r["nm"]),
                     oos=round(oos), color=palette[min(len(palette) - 1, int(oos / 100 * (len(palette) - 1)))]))
source = ColumnDataSource(dict(
    x=[d["x"] for d in recs], y=[d["y"] for d in recs], name=[d["name"] for d in recs],
    tag=[d["tag"] for d in recs], oos=[d["oos"] for d in recs], color=[d["color"] for d in recs]))

TOOLS = "hover,pan,wheel_zoom,box_zoom,reset,save"
p = figure(tools=TOOLS, toolbar_location="above", width=900, height=560,
           title="Davidson operators: parcels vs average value (colored by out-of-state share)")
p.background_fill_color = "#efefef"
p.xaxis.axis_label = "average parcel value ($000s)"
p.yaxis.axis_label = "parcels held"
p.grid.grid_line_color = "white"
p.hover.tooltips = [("operator", "@name"), ("parcels", "@y"),
                    ("avg value", "@x{$0,0}k"), ("out-of-state", "@oos%")]
p.scatter("x", "y", size=14, source=source, color="color", line_color="black", alpha=0.9)
p.add_layout(LabelSet(x="x", y="y", text="tag", y_offset=8, text_font_size="10px",
                      text_color="#555555", source=source, text_align="center"))

write(p, os.path.join(os.path.dirname(__file__), "b20_elements_labels.html"),
      "Labelled scatter — Davidson operators")
