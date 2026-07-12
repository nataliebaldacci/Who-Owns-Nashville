"""Shared Nashville sample data + save helper for the Bokeh cookbook scripts."""
from bokeh.plotting import save, output_file
from bokeh.resources import INLINE

OPS = ["Progress", "AMH", "Amherst", "Regent", "Normandy", "Tricon"]
TN  = [290, 274, 204, 584, 346, 65]
OOS = [925, 908, 490, 12, 2, 233]
PARCELS = [1215, 1182, 699, 642, 348, 298]
AVG_VALUE_K = [373, 434, 448, 190, 433, 439]
TIER = ["Institutional", "Institutional", "Institutional", "Builder/BTR", "Builder/BTR", "Institutional"]
OP_COLORS = ["#e6194b", "#2166ac", "#1a9850", "#f0af1e", "#911eb4", "#4fa0bd"]

def write(p, fname, title):
    output_file(fname, title=title)
    save(p, resources=INLINE)
    print("wrote", fname)
