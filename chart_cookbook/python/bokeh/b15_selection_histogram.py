"""Selection histogram (Bokeh demo.bokeh.org/selection_histogram, standalone).
A central scatter with a marginal histogram above (x) and to the right (y). Each
histogram shows the full distribution in grey plus a highlighted overlay that
recomputes live as you Box- or Lasso-select points in the scatter. The official
demo uses a Bokeh server callback; this is a self-contained HTML version driven
by CustomJS so it needs no server. Real data: Davidson block groups — x = poverty
rate, y = institutional ownership rate, one point per block group."""
import os, sys
import numpy as np
import geopandas as gpd
from bokeh.layouts import gridplot
from bokeh.models import ColumnDataSource, CustomJS, BoxSelectTool, LassoSelectTool
from bokeh.plotting import figure
sys.path.insert(0, os.path.dirname(__file__))
from _shared import write

ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
bg = gpd.read_file(os.path.join(ROOT, "institutional_by_blockgroup.geojson"))
bg = bg[(bg["pov"].notna()) & (bg["rate"].notna())]
x = bg["pov"].to_numpy(dtype=float)
y = bg["rate"].clip(upper=np.nanpercentile(bg["rate"], 99)).to_numpy(dtype=float)
source = ColumnDataSource(data=dict(x=x, y=y))

TOOLS = "pan,wheel_zoom,box_select,lasso_select,reset"
NAVY, GREY, GOLD = "#1c458c", "#cfd6df", "#f0af1e"

# --- central scatter ---
p = figure(width=600, height=600, tools=TOOLS, active_drag="box_select",
           x_axis_label="Poverty rate (%)", y_axis_label="Institutional ownership rate (%)",
           title="Select points to update the marginal histograms")
r = p.scatter("x", "y", source=source, size=7, color=NAVY, alpha=0.55,
              selection_color=GOLD, nonselection_alpha=0.15, nonselection_color=NAVY)

# --- precompute full histograms ---
hedges = np.linspace(x.min(), x.max(), 21)
vedges = np.linspace(y.min(), y.max(), 21)
htop_all, _ = np.histogram(x, bins=hedges)
vright_all, _ = np.histogram(y, bins=vedges)

# top histogram (x)
ph = figure(width=600, height=160, x_range=p.x_range, min_border=10,
            y_axis_location="right", title=None, tools="")
ph.xgrid.grid_line_color = None; ph.yaxis.major_label_orientation = np.pi / 4
ph.background_fill_color = "#fafafa"
ph.quad(bottom=0, left=hedges[:-1], right=hedges[1:], top=htop_all,
        color=GREY, line_color="white")
sh_top = ColumnDataSource(dict(left=hedges[:-1], right=hedges[1:], top=np.zeros(len(hedges) - 1)))
ph.quad(bottom=0, left="left", right="right", top="top", source=sh_top,
        color=GOLD, alpha=0.7, line_color="white")

# right histogram (y)
pv = figure(width=160, height=600, y_range=p.y_range, min_border=10, tools="")
pv.ygrid.grid_line_color = None; pv.xaxis.major_label_orientation = np.pi / 4
pv.background_fill_color = "#fafafa"
pv.quad(left=0, bottom=vedges[:-1], top=vedges[1:], right=vright_all,
        color=GREY, line_color="white")
sh_right = ColumnDataSource(dict(bottom=vedges[:-1], top=vedges[1:], right=np.zeros(len(vedges) - 1)))
pv.quad(left=0, bottom="bottom", top="top", right="right", source=sh_right,
        color=GOLD, alpha=0.7, line_color="white")

# --- CustomJS: recompute selected histograms on selection change ---
cb = CustomJS(args=dict(source=source, sh_top=sh_top, sh_right=sh_right,
                        hedges=hedges.tolist(), vedges=vedges.tolist()), code="""
    const inds = source.selected.indices;
    const x = source.data['x'], y = source.data['y'];
    function hist(vals, idxs, edges) {
        const n = edges.length - 1;
        const c = new Array(n).fill(0);
        for (const i of idxs) {
            const v = vals[i];
            for (let b = 0; b < n; b++) {
                if (v >= edges[b] && (v < edges[b+1] || (b === n-1 && v <= edges[b+1]))) { c[b]++; break; }
            }
        }
        return c;
    }
    sh_top.data['top'] = hist(x, inds, hedges);
    sh_right.data['right'] = hist(y, inds, vedges);
    sh_top.change.emit();
    sh_right.change.emit();
""")
source.selected.js_on_change("indices", cb)

layout = gridplot([[ph, None], [p, pv]], merge_tools=False)
write(layout, os.path.join(os.path.dirname(__file__), "b15_selection_histogram.html"),
      "Selection histogram — Davidson block groups")
