"""Log-axis plot (Bokeh) — growth functions on a log y-axis with a legend."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__)); from _shared import write
import numpy as np
from bokeh.plotting import figure
x = np.linspace(0.1, 5, 80)
p = figure(title="Log axis example", y_axis_type="log", x_range=(0,5), y_range=(0.001, 1e22), background_fill_color="#fafafa", width=760, height=420)
p.line(x, np.sqrt(x), legend_label="y=sqrt(x)", line_color="tomato", line_dash="dashed")
p.line(x, x, legend_label="y=x"); p.scatter(x, x, legend_label="y=x")
p.line(x, x**2, legend_label="y=x^2"); p.scatter(x, x**2, fill_color=None, line_color="olivedrab", legend_label="y=x^2")
p.line(x, 10**x, legend_label="y=10^x", line_color="gold", line_width=2)
p.legend.location = "top_left"
write(p, "b11_logplot.html", "Log plot")
