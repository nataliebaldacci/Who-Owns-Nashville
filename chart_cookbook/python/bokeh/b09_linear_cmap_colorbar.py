"""Scatter with linear color mapping + colorbar (Bokeh) — parcels colored by value."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__)); from _shared import write
import numpy as np
from bokeh.plotting import figure, ColumnDataSource
from bokeh.transform import linear_cmap
rng = np.random.default_rng(3); n=400
x = rng.normal(700, 300, n).clip(10); y = x*0.35 + rng.normal(0, 60, n); val = x*0.3 + rng.normal(0,20,n)
src = ColumnDataSource(dict(x=x, y=y, val=val))
cmap = linear_cmap("val", palette="Viridis256", low=val.min(), high=val.max())
p = figure(width=780, height=420, title="Parcels colored by value (linear_cmap)", toolbar_location=None, tools="")
r = p.scatter("x", "y", source=src, size=9, color=cmap, alpha=0.8)
p.add_layout(r.construct_color_bar(padding=0), "right")
p.xaxis.axis_label = "Parcels"; p.yaxis.axis_label = "Dwelling units"
write(p, "b09_linear_cmap_colorbar.html", "linear_cmap + colorbar")
