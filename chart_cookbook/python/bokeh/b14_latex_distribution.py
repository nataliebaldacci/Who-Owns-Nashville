"""Histogram + PDF with LaTeX/mathtext axis labels (Bokeh) — sale-price distribution."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__)); from _shared import write
import numpy as np
from bokeh.models import TeX
from bokeh.plotting import figure
rng = np.random.default_rng(825914); x = rng.normal(4.7, 12.3, 1000); scaled = (x-x.mean())/x.std()
bins = np.linspace(-3,3,40); hist, edges = np.histogram(scaled, density=True, bins=bins)
p = figure(width=680, height=420, title="Standardized Sale-Price Distribution", toolbar_location=None)
p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], fill_color="#4fa0bd", line_color="white", legend_label="1000 parcels")
xs = np.linspace(-3,3,100); p.line(xs, np.exp(-0.5*xs**2)/np.sqrt(2*np.pi), line_width=2, line_color="#1c458c", legend_label="PDF")
p.xaxis.ticker=[-3,-2,-1,0,1,2,3]
p.xaxis.major_label_overrides={-3:TeX(r"\overline{x}-3\sigma"),0:TeX(r"\overline{x}"),3:TeX(r"\overline{x}+3\sigma")}
p.y_range.start=0
write(p, "b14_latex_distribution.html", "LaTeX distribution")
