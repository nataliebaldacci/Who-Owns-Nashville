"""Scatter marker gallery (Bokeh) — the available marker glyph types."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__)); from _shared import write
from bokeh.plotting import figure
markers = ["circle","square","triangle","diamond","hex","inverted_triangle","plus","star","asterisk","cross"]
p = figure(width=780, height=360, title="Bokeh marker types", toolbar_location=None)
for i, m in enumerate(markers):
    p.scatter([i], [0], marker=m, size=22, fill_color="#f0af1e", line_color="#1c458c")
    p.text([i], [0.4], text=[m], text_font_size="9px", text_align="center")
p.y_range.start = -1; p.y_range.end = 1.5; p.yaxis.visible = False; p.xaxis.visible = False
p.grid.grid_line_color = None
write(p, "b08_markers.html", "Markers")
