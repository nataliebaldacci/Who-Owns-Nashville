"""
Shared house-style palettes for the chart cookbook.

Four styles are available; call apply_style(name) at the top of any script,
BEFORE creating the figure, to set the matplotlib rcParams + color cycle:

    from styles.won_styles import apply_style, palette
    apply_style("jchs")            # or "crs", "won", "hud"
    colors = palette("jchs")

Styles
------
- "won"  : Who Owns Nashville brand (navy #1c458c + gold #f0af1e).
- "hud"  : HUD county-chart look (grey card, dark plot frame, sans-serif).
- "jchs" : Harvard Joint Center for Housing Studies (slate blue + burnt orange
           + sage + mustard + plum). Read from the JCHS OOXML/CSS bundles.
- "crs"  : Congressional Research Service report figures (Highcharts/Office
           palette: steel blue, orange, grey, gold; tan bars for stock charts).
"""
import matplotlib as mpl
from cycler import cycler

PALETTES = {
    # Who Owns Nashville brand + stable per-operator qualitative set
    "won":  ["#1c458c", "#f0af1e", "#4fa0bd", "#d7263d", "#1a9850", "#911eb4", "#16a085", "#cf307a"],
    # HUD default-theme series colors
    "hud":  ["#AFD8F8", "#F6BD0F", "#8BBA00", "#1c458c", "#d7263d", "#5A5A5A"],
    # Harvard JCHS core palette (ranked by use across 19 decks)
    "jchs": ["#508DA6", "#C14D00", "#76AD99", "#E9C002", "#653052", "#002060", "#5A5A5A"],
    # CRS / congress.gov Highcharts (Office-family) palette
    "crs":  ["#2E75B6", "#ED7D31", "#A5A5A5", "#FFC000", "#4472C4", "#70AD47", "#C00000"],
}

# A few named accents scripts may want by hand
ACCENTS = {
    "jchs_slate": "#508DA6", "jchs_orange": "#C14D00", "jchs_sage": "#76AD99",
    "jchs_mustard": "#E9C002", "jchs_plum": "#653052", "jchs_ink": "#231F20",
    "crs_tan": "#D2D1AB", "crs_blue": "#2E75B6", "crs_orange": "#ED7D31",
    "won_navy": "#1c458c", "won_gold": "#f0af1e",
}

# JCHS sequential ramps for choropleths (from the interactive bundles)
RAMPS = {
    "jchs_blue":   ["#D6E5EB", "#93BACB", "#659DB5", "#4E7686", "#507687"],
    "jchs_orange": ["#F3C669", "#F09E3D", "#F89F5C", "#EA7923", "#C14D00"],
    "won_ylorbr":  ["#ffffd4", "#fee391", "#fec44f", "#fe9929", "#cc4c02"],
    "won_blues":   ["#eff3ff", "#bdd7e7", "#6baed6", "#3182bd", "#08519c"],
}

_TEXT = {"jchs": "#231F20", "crs": "#333333", "won": "#20303f", "hud": "#333333"}
_GRID = {"jchs": "#D9D9D9", "crs": "#e6e6e6", "won": "#d6ddea", "hud": "#e6e6e6"}


def palette(name="won"):
    """Return the ordered list of series colors for a style."""
    return list(PALETTES[name])


def apply_style(name="won"):
    """Set matplotlib rcParams + color cycle for the named house style."""
    ink = _TEXT.get(name, "#333333")
    grid = _GRID.get(name, "#e6e6e6")
    mpl.rcParams.update({
        "axes.prop_cycle": cycler(color=PALETTES[name]),
        "figure.facecolor": "#ffffff",
        "axes.facecolor": "#ffffff",
        "axes.edgecolor": ink,
        "axes.labelcolor": ink,
        "axes.titlecolor": ink,
        "axes.titleweight": "bold",
        "axes.grid": True,
        "axes.grid.axis": "y",
        "grid.color": grid,
        "grid.linewidth": 0.8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "text.color": ink,
        "xtick.color": ink,
        "ytick.color": ink,
        "font.size": 11,
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica Neue", "Arial", "DejaVu Sans"],
    })
    return palette(name)
