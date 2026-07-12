"""Linear vs log color mapping grid (Bokeh)."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__)); from _shared import write
import numpy as np
from bokeh.layouts import gridplot
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.transform import linear_cmap, log_cmap
x = np.random.default_rng(1).random(1500)*1000; y = np.random.default_rng(2).normal(5,2,1500)
src = ColumnDataSource(dict(x=x, y=y))
def mk(mapper, pal):
    cmap = mapper("x", palette=pal, low=1, high=1000); axt = mapper.__name__.split("_")[0]
    p = figure(x_range=(1,1000), title=f"{pal} · {mapper.__name__}", toolbar_location=None, tools="", x_axis_type=axt, width=390, height=280)
    r = p.scatter("x","y",source=src,color=cmap,alpha=0.7); p.add_layout(r.construct_color_bar(padding=0), "below"); return p
grid = gridplot([[mk(linear_cmap,"Viridis256"), mk(log_cmap,"Viridis256")],
                 [mk(linear_cmap,"Viridis6"),   mk(log_cmap,"Viridis6")]], toolbar_location=None)
write(grid, "b10_color_mappers.html", "Color mappers")
