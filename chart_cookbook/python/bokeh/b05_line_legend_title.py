"""Multi-line time series with a styled legend title (Bokeh)."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__)); from _shared import write
from bokeh.palettes import Spectral4
from bokeh.plotting import figure
years = list(range(2015, 2025))
series = {"Progress":[60,110,180,260,340,300,250,220,200,190],
          "AMH":[80,130,190,250,320,280,210,180,170,160],
          "Amherst":[40,70,120,170,230,190,150,120,110,100],
          "Tricon":[10,20,40,70,110,90,70,55,50,48]}
p = figure(width=820, height=300, title="Acquisitions by Operator over Time")
for (name, ys), color in zip(series.items(), Spectral4):
    p.line(years, ys, line_width=2, color=color, legend_label=name)
p.legend.location = "top_left"; p.legend.title = "Operator"
p.legend.title_text_font_style = "bold"; p.legend.title_text_font_size = "14px"
write(p, "b05_line_legend_title.html", "Line + legend title")
