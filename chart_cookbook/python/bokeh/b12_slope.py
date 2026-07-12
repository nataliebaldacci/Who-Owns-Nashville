"""Scatter with a Slope regression line annotation (Bokeh)."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__)); from _shared import write
import numpy as np
from bokeh.models import Slope
from bokeh.plotting import figure
rng = np.random.default_rng(7); sqft = rng.normal(1900,400,300); price = sqft*0.22 + rng.normal(0,40,300)
m, b = np.polyfit(sqft, price, 1)
p = figure(width=760, height=440, title=f"Price vs size with fit (slope={m:.3f})", background_fill_color="#fafafa")
p.scatter(sqft, price, size=8, alpha=0.4, color="#4fa0bd")
p.add_layout(Slope(gradient=m, y_intercept=b, line_color="#d7263d", line_width=3, line_dash="dashed"))
p.xaxis.axis_label = "Living area (sqft)"; p.yaxis.axis_label = "Sale price ($000s)"
write(p, "b12_slope.html", "Slope")
