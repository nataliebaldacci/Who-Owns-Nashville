"""Dodged bar chart (Bokeh) — TN vs out-of-state holdings side by side per operator."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__)); from _shared import OPS, TN, OOS, write
from bokeh.plotting import figure, ColumnDataSource
from bokeh.transform import dodge
src = ColumnDataSource(dict(ops=OPS, tn=TN, oos=OOS))
p = figure(x_range=OPS, height=380, width=760, title="In-State vs Out-of-State Holdings (dodged)",
           toolbar_location=None, tools="", tooltips="@ops: $name = @$name")
p.vbar(x=dodge("ops", -0.17, range=p.x_range), top="tn", width=0.3, source=src,
       color="#f0af1e", legend_label="In-State (TN)", name="tn")
p.vbar(x=dodge("ops", 0.17, range=p.x_range), top="oos", width=0.3, source=src,
       color="#1c458c", legend_label="Out-of-State", name="oos")
p.y_range.start = 0; p.xgrid.grid_line_color = None; p.legend.location = "top_right"
write(p, "b01_dodged_bars.html", "Dodged bars")
