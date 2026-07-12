"""Crosstab adjacent hbar (Bokeh) — owner-type composition within each investor tier."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__)); from _shared import write
import pandas as pd
from bokeh.core.properties import value
from bokeh.plotting import figure, ColumnDataSource
from bokeh.transform import cumsum, factor_cmap
# synthetic composition: share of each owner type within tier
rows = pd.DataFrame({"Individual":[.62,.41],"Corporate":[.22,.34],"Trust":[.10,.15],"Other":[.06,.10]},
                    index=["Small tier","Large tier"])
src = ColumnDataSource(rows.T); tiers = list(rows.index); types = list(rows.columns)
p = figure(y_range=types, x_range=(0,1.05), height=340, width=720, tools="", x_axis_location=None,
           toolbar_location=None, title="Owner-type share within tier (crosstab)")
p.grid.grid_line_color = None
for t in types:
    p.hbar(y=value(t), left=cumsum(t, include_zero=True), right=cumsum(t), source=src, height=0.85,
           color=factor_cmap("index", "MediumContrast4", src.data["index"]))
write(p, "b04_crosstab_hbar.html", "Crosstab hbar")
