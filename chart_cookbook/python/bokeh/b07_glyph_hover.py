"""Scatter with hover highlight (Bokeh) — sale price vs living area."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__)); from _shared import write
import numpy as np
from bokeh.models import HoverTool
from bokeh.plotting import figure
rng = np.random.default_rng(5); sqft = rng.normal(1900, 400, 400); price = sqft*0.22 + rng.normal(0, 40, 400)
p = figure(width=780, height=420, title="Hover over points — price vs size", background_fill_color="#fafafa")
cr = p.scatter(sqft, price, size=12, fill_color="#4fa0bd", alpha=0.25, line_color=None,
               hover_fill_color="#1c458c", hover_alpha=0.8, hover_line_color="white")
p.add_tools(HoverTool(tooltips=None, renderers=[cr], mode="hline"))
p.xaxis.axis_label = "Living area (sqft)"; p.yaxis.axis_label = "Sale price ($000s)"
write(p, "b07_glyph_hover.html", "Glyph hover")
