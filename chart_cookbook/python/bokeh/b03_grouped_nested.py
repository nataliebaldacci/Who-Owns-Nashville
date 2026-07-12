"""Grouped/nested bar chart (Bokeh) — parcels by tier then operator, factor_cmap + hover."""
import sys, os; sys.path.insert(0, os.path.dirname(__file__)); from _shared import OPS, PARCELS, TIER, write
import pandas as pd
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.palettes import MediumContrast3
df = pd.DataFrame(dict(op=OPS, parcels=PARCELS, tier=TIER))
group = df.groupby(["tier", "op"])
cmap = factor_cmap("tier_op", palette=MediumContrast3, factors=sorted(df.tier.unique()), end=1)
p = figure(width=800, height=340, title="Parcels by Investor Tier and Operator (nested)",
           x_range=group, toolbar_location=None, tooltips=[("Parcels", "@parcels_mean"), ("Tier, Op", "@tier_op")])
p.vbar(x="tier_op", top="parcels_mean", width=1, source=group, line_color="white", fill_color=cmap)
p.y_range.start = 0; p.x_range.range_padding = 0.05; p.xgrid.grid_line_color = None
p.xaxis.major_label_orientation = 1.2; p.outline_line_color = None
write(p, "b03_grouped_nested.html", "Grouped nested bars")
