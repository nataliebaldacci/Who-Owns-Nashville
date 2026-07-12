"""Basemap tiles (Bokeh) — CartoDB Positron behind operator points (web mercator).
Tiles load from CDN; renders in a browser like the site's Leaflet maps."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__)); from _shared import OPS, PARCELS, OP_COLORS, write
import numpy as np
from bokeh.plotting import figure, ColumnDataSource
def merc(lon, lat):
    R=6378137.0; return lon*R*np.pi/180.0, np.log(np.tan((90+lat)*np.pi/360.0))*R
lons=[-86.72,-86.78,-86.68,-86.80,-86.74,-86.70]; lats=[36.10,36.16,36.05,36.20,36.12,36.02]
xs, ys = zip(*[merc(a,b) for a,b in zip(lons,lats)])
src = ColumnDataSource(dict(x=xs, y=ys, op=OPS, size=[p/40 for p in PARCELS], color=OP_COLORS))
p = figure(x_axis_type="mercator", y_axis_type="mercator", width=760, height=620,
           title="Operator holdings on CartoDB Positron", tooltips=[("Operator","@op")])
p.add_tile("CartoDB Positron", retina=True)
p.scatter("x","y",source=src, size="size", color="color", alpha=0.8, line_color="white")
write(p, "b13_tile_map.html", "Tile map")
