"""Stacked bar chart (Bokeh) — TN + out-of-state stacked per operator."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__)); from _shared import OPS, TN, OOS, write
from bokeh.plotting import figure, ColumnDataSource
src = ColumnDataSource(dict(ops=OPS, tn=TN, oos=OOS))
p = figure(x_range=OPS, height=380, width=760, title="Holdings by Owner Location (stacked)",
           toolbar_location=None, tools="", tooltips="$name: @$name")
p.vbar_stack(["tn", "oos"], x="ops", width=0.7, source=src,
             color=["#f0af1e", "#1c458c"], legend_label=["In-State (TN)", "Out-of-State"])
p.y_range.start = 0; p.xgrid.grid_line_color = None; p.legend.location = "top_right"
write(p, "b02_stacked_bars.html", "Stacked bars")
