"""Who Owns Nashville — LOCKED cookbook palette (Palettable / CARTOColors).

The single source of truth for cookbook colors. Import from here so every figure
stays consistent.

    from styles.locked_palette import NAVY, GOLD, PRISM, OPERATOR_COLORS, RAMPS, op_color

Brand:      NAVY #1c458c (primary), GOLD #f0af1e (callout).
Operators:  Prism_10 shades, hand-assigned so Progress = red, American = blue.
            Use op_color(name) to get an operator's locked color.
Series:     PRISM (Prism_10) for generic categorical chart series (non-operator).
Sequential: institutional = SunsetDark_7, institutional_alt = YlOrRd_6,
            tenure = Blues_6, cost_burden = BuPu_6.
Diverging:  geyser = Geyser_7 (default), diverging_alt = RdBu_9.
Report:     JCHS set (slate/orange/sage/mustard) for State-of-the-Nation looks.
"""
import palettable.cartocolors.qualitative as _q
import palettable.cartocolors.sequential as _seq
import palettable.cartocolors.diverging as _div
import palettable.colorbrewer.sequential as _cb_seq
import palettable.colorbrewer.diverging as _cb_div

# ---- brand ----
NAVY = "#1c458c"
NAVY_DK = "#16357a"
GOLD = "#f0af1e"
LIGHTBLUE = "#4fa0bd"
ACCENT_RED = "#d7263d"
PANEL = "#eef4fb"
TEXT = "#20303f"
NODATA = "#c9ced6"

# ---- generic categorical series (non-operator) ----
PRISM = _q.Prism_10.hex_colors   # ['#5F4690','#1D6996','#38A6A5','#0F8554','#73AF48',
                                 #  '#EDAD08','#E17C05','#CC503E','#94346E','#6F4070']

# ---- operators: Prism_10 shades, hand-assigned (Progress=red, American=blue) ----
OPERATOR_COLORS = {
    "Progress Residential":    "#CC503E",  # Prism red
    "American Homes 4 Rent":   "#1D6996",  # Prism blue
    "Amherst Residential":     "#38A6A5",  # Prism teal
    "Starwood Capital Group":  "#0F8554",  # Prism green
    "Tricon Residential":      "#73AF48",  # Prism light green
    "Invitation Homes":        "#94346E",  # Prism plum
    "VineBrook Homes":         "#5F4690",  # Prism purple
    "Rithm Capital":           "#E17C05",  # Prism orange
    "Brookfield":              "#EDAD08",  # Prism gold
    "Regent Homes":            "#6F4070",  # Prism dark purple
    "Other corporate":         NODATA,     # grey
}
# common short forms / aliases -> canonical key
_ALIASES = {
    "progress": "Progress Residential", "pretium": "Progress Residential",
    "amh": "American Homes 4 Rent", "american homes": "American Homes 4 Rent",
    "amherst": "Amherst Residential", "main street renewal": "Amherst Residential",
    "starwood": "Starwood Capital Group", "invitation": "Invitation Homes",
    "tricon": "Tricon Residential", "vinebrook": "VineBrook Homes",
    "rithm": "Rithm Capital", "brookfield": "Brookfield", "maymont": "Brookfield",
    "regent": "Regent Homes", "firstkey": "#134e4e", "other": "Other corporate",
}

def op_color(name, default="#c9ced6"):
    """Locked color for an operator, tolerant of short forms; grey if unknown."""
    if not name:
        return default
    if name in OPERATOR_COLORS:
        return OPERATOR_COLORS[name]
    low = name.lower()
    for key, canon in _ALIASES.items():
        if key in low:
            return canon if canon.startswith("#") else OPERATOR_COLORS[canon]
    for canon in OPERATOR_COLORS:
        if canon.lower() in low or low in canon.lower():
            return OPERATOR_COLORS[canon]
    return default

# ---- sequential ramps (role -> palettable palette) ----
RAMPS = {
    "institutional":     _seq.SunsetDark_7,   # institutional / corporate share
    "institutional_alt": _cb_seq.YlOrRd_6,    # warm alt, closest to old YlOrBr
    "tenure":            _cb_seq.Blues_6,      # tenure / ownership
    "cost_burden":       _cb_seq.BuPu_6,       # cost / rent burden
}
# ---- diverging ----
DIVERGING = {
    "geyser":        _div.Geyser_7,   # default (teal <-> orange)
    "diverging_alt": _cb_div.RdBu_9,  # red <-> blue alt
}

def ramp(role):
    """Matplotlib LinearSegmentedColormap for a sequential/diverging role."""
    from matplotlib.colors import LinearSegmentedColormap
    pal = RAMPS.get(role) or DIVERGING.get(role)
    if pal is None:
        raise KeyError(f"unknown ramp role: {role}")
    return LinearSegmentedColormap.from_list(role, pal.hex_colors)

# ---- report (JCHS) ----
JCHS = {"slate": "#508DA6", "orange": "#C14D00", "sage": "#76AD99",
        "mustard": "#FFC52F", "plum": "#653052", "ink": "#231F20"}


if __name__ == "__main__":  # render the locked reference sheet
    import matplotlib; matplotlib.use("Agg")
    import os, numpy as np, matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap

    rows = []
    rows.append(("NAVY  (brand primary)", [NAVY]))
    rows.append(("GOLD  (brand callout)", [GOLD]))
    rows.append(("Operators (Prism_10, locked)", list(OPERATOR_COLORS.values())))
    rows.append(("PRISM_10  (generic series)", PRISM))
    rows.append(("SunsetDark_7  (institutional)", RAMPS["institutional"].hex_colors))
    rows.append(("YlOrRd_6  (institutional alt)", RAMPS["institutional_alt"].hex_colors))
    rows.append(("Blues_6  (tenure)", RAMPS["tenure"].hex_colors))
    rows.append(("BuPu_6  (cost burden)", RAMPS["cost_burden"].hex_colors))
    rows.append(("Geyser_7  (diverging)", DIVERGING["geyser"].hex_colors))
    rows.append(("RdBu_9  (diverging alt)", DIVERGING["diverging_alt"].hex_colors))

    fig, ax = plt.subplots(figsize=(13, 9)); ax.axis("off")
    for r, (label, hexes) in enumerate(rows):
        y = len(rows) - r
        n = len(hexes)
        for i, hx in enumerate(hexes):
            ax.add_patch(plt.Rectangle((3 + i * 9.0 / n, y), 9.0 / n, 0.8, color=hx))
        ax.text(2.8, y + 0.4, label, ha="right", va="center", fontsize=11, fontweight="bold")
    # operator name labels under the operator row
    orow_y = len(rows) - 2
    for i, name in enumerate(OPERATOR_COLORS):
        short = name.replace(" Residential", "").replace(" Capital Group", "").replace(" Homes", "")
        ax.text(3 + (i + 0.5) * 9.0 / len(OPERATOR_COLORS), orow_y - 0.15, short,
                ha="center", va="top", fontsize=6.2, rotation=32, color="#333")
    ax.set_xlim(0, 12.5); ax.set_ylim(0, len(rows) + 2.4)
    ax.text(3, len(rows) + 1.7, "Who Owns Nashville — LOCKED cookbook palette",
            fontsize=16, fontweight="bold")
    ax.text(3, len(rows) + 1.2, "Prism_10 operators (Progress=red, American=blue) · "
            "SunsetDark/YlOrRd/Blues/BuPu sequential · Geyser/RdBu diverging",
            fontsize=9.5, color="#555")
    out = os.path.join(os.path.dirname(__file__), "..", "figures", "locked_palette.png")
    plt.savefig(out, dpi=140, bbox_inches="tight")
    print("wrote", os.path.abspath(out))
