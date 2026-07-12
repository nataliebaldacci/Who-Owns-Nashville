"""Population pyramid with a Select (demo.bokeh.org/population, standalone). A
back-to-back horizontal bar chart: one group's bars grow left (negative), the
other's grow right, sharing a categorical y-axis. A Select widget swaps what
defines the two sides, recomputing the bars via CustomJS. The official demo is a
Bokeh server app; this is a self-contained HTML version. Real data: Davidson
corporate SFR parcels by bedroom count, split two ways."""
import os, sys, json, collections
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Select, CustomJS, NumeralTickFormatter
from bokeh.plotting import figure
sys.path.insert(0, os.path.dirname(__file__))
from _shared import write

ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
props = [f["properties"] for f in
         json.load(open(os.path.join(ROOT, "Davidson_Active_Corporate_SFR_Detail.geojson")))["features"]]

BEDS = ["1", "2", "3", "4", "5", "6+"]
def bed_bin(b): return "6+" if b.isdigit() and int(b) >= 6 else (b if b in BEDS else None)

# two split options; each maps to (left_label, right_label, predicate on a parcel -> is_right?)
def vintage_side(p): return str(p.get("ybuilt", "")).isdigit() and int(p["ybuilt"]) >= 2000
def type_side(p):    return (p.get("ptype") or "") == "Single Family"

SPLITS = {
    "Vintage: pre-2000  vs  2000+": ("Built pre-2000", "Built 2000+", vintage_side),
    "Type: other  vs  single-family": ("Duplex / Condo / other", "Single Family", type_side),
}

# precompute left/right counts per bedroom bin for each split option
data = {}
labels = {}
for name, (lname, rname, pred) in SPLITS.items():
    left = collections.Counter(); right = collections.Counter()
    for p in props:
        bb = bed_bin(str(p.get("beds", "")))
        if bb is None:
            continue
        (right if pred(p) else left)[bb] += 1
    data[name] = dict(left=[-left[b] for b in BEDS], right=[right[b] for b in BEDS])
    labels[name] = [lname, rname]

first = list(SPLITS)[0]
source = ColumnDataSource(dict(beds=BEDS, left=data[first]["left"], right=data[first]["right"]))

p = figure(y_range=BEDS, height=420, width=680, toolbar_location=None,
           x_axis_label="parcels  (← left group      right group →)",
           y_axis_label="Bedrooms", title="Corporate parcels by bedroom count")
p.hbar(y="beds", right="right", height=0.7, source=source, color="#1c458c", legend_label=labels[first][1])
p.hbar(y="beds", right="left", height=0.7, source=source, color="#f0af1e", legend_label=labels[first][0])
p.xaxis.formatter = NumeralTickFormatter(format="0,0")
p.xgrid.grid_line_color = None
p.legend.location = "bottom_right"

sel = Select(title="Split the two sides by:", value=first, options=list(SPLITS))
cb = CustomJS(args=dict(source=source, data=data, sel=sel), code="""
    const d = data[sel.value];
    source.data['left'] = d.left;
    source.data['right'] = d.right;
    source.change.emit();
""")
sel.js_on_change("value", cb)

write(column(sel, p), os.path.join(os.path.dirname(__file__), "b18_population_pyramid.html"),
      "Population pyramid — Davidson corporate parcels")
