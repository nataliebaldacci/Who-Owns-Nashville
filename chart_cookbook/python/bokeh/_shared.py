"""Shared Nashville sample data + save helper for the Bokeh cookbook scripts."""
from bokeh.plotting import save, output_file
from bokeh.resources import INLINE

OPS = ["Progress", "AMH", "Amherst", "Regent", "Normandy", "Tricon"]
TN  = [290, 274, 204, 584, 346, 65]
OOS = [925, 908, 490, 12, 2, 233]
PARCELS = [1215, 1182, 699, 642, 348, 298]
AVG_VALUE_K = [373, 434, 448, 190, 433, 439]
TIER = ["Institutional", "Institutional", "Institutional", "Builder/BTR", "Builder/BTR", "Institutional"]
# locked operator colors (Prism_10 shades; see styles/locked_palette.py)
# Progress=red, AMH=blue, Amherst=teal, Regent=dark-purple, (Normandy)=grey, Tricon=light-green
OP_COLORS = ["#CC503E", "#1D6996", "#38A6A5", "#6F4070", "#c9ced6", "#73AF48"]

def write(p, fname, title):
    output_file(fname, title=title)
    save(p, resources=INLINE)
    print("wrote", fname)
