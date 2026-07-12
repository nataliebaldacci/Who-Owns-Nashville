"""
Unified palette accessor for the chart cookbook.

Brings every major color-scheme library under one call, get():

    from styles.palettes import get, CURATED
    get("jchs")                 # cookbook house styles (won/jchs/crs/hud)
    get("Category10")           # Bokeh categorical
    get("Set2")                 # ColorBrewer via palettable
    get("Bold", n=8)            # CARTOColors qualitative
    get("Thermal", n=7)         # cmocean sequential
    get("viridis", n=6)         # any matplotlib colormap, sampled to n
    get("Acadia")               # any of pypalettes' 2,500+ palettes

Resolution order: cookbook house styles -> Bokeh categoricals ->
matplotlib colormap -> palettable (searched across families) ->
pypalettes.get_hex(). Returns a list of hex strings.

Underlying libraries (see requirements.txt):
  palettable  - ColorBrewer, CARTOColors, cmocean, Scientific, Tableau,
                Wes Anderson, cubehelix, mycarta, lightbartlein ...
  pypalettes  - 2,500+ palettes (get_hex / load_cmap / show_cmap)
  matplotlib  - all built-in colormaps (viridis, cividis, magma, coolwarm ...)
  bokeh       - Category10/20 hardcoded below (no bokeh dependency needed)
"""
import matplotlib.pyplot as plt
from matplotlib.colors import to_hex
from .won_styles import PALETTES as HOUSE

# --- Bokeh categorical palettes (hardcoded; identical to bokeh.palettes) ---
BOKEH = {
    "Category10": ["#1f77b4","#ff7f0e","#2ca02c","#d62728","#9467bd",
                   "#8c564b","#e377c2","#7f7f7f","#bcbd22","#17becf"],
    "Category20": ["#1f77b4","#aec7e8","#ff7f0e","#ffbb78","#2ca02c","#98df8a",
                   "#d62728","#ff9896","#9467bd","#c5b0d5","#8c564b","#c49c94",
                   "#e377c2","#f7b6d2","#7f7f7f","#c7c7c7","#bcbd22","#dbdb8d",
                   "#17becf","#9edae5"],
    "Bokeh8": ["#1f77b4","#ff7f0e","#2ca02c","#d62728","#9467bd","#8c564b","#e377c2","#7f7f7f"],
}


def _from_matplotlib(name, n):
    cmap = plt.get_cmap(name)
    n = n or (cmap.N if cmap.N <= 20 else 8)
    if hasattr(cmap, "colors") and len(getattr(cmap, "colors", [])) <= 40 and not n:
        return [to_hex(c) for c in cmap.colors]
    return [to_hex(cmap(i / max(n - 1, 1))) for i in range(n)]


def _from_palettable(name, n):
    import palettable
    # search common families for an exact or N-suffixed match
    families = [
        "colorbrewer.sequential", "colorbrewer.diverging", "colorbrewer.qualitative",
        "cartocolors.sequential", "cartocolors.diverging", "cartocolors.qualitative",
        "cmocean.sequential", "cmocean.diverging", "scientific.sequential",
        "scientific.diverging", "tableau", "wesanderson", "cubehelix", "mycarta",
    ]
    import importlib
    want = name.lower()
    for fam in families:
        try:
            mod = importlib.import_module("palettable." + fam)
        except Exception:
            continue
        for attr in dir(mod):
            base = attr.rsplit("_", 1)[0].lower()
            if base == want or attr.lower() == want:
                pal = getattr(mod, attr)
                if hasattr(pal, "hex_colors"):
                    return pal.hex_colors
    return None


def get(name, n=None):
    """Resolve a palette name to a list of hex colors from any known library."""
    if name in HOUSE:
        cols = list(HOUSE[name])
        return cols[:n] if n else cols
    if name in BOKEH:
        cols = list(BOKEH[name])
        return cols[:n] if n else cols
    # matplotlib colormap?
    try:
        return _from_matplotlib(name, n)
    except Exception:
        pass
    # palettable family search
    try:
        cols = _from_palettable(name, n)
        if cols:
            return cols[:n] if n else cols
    except Exception:
        pass
    # pypalettes (2,500+)
    try:
        from pypalettes import load_cmap
        cols = [c[:7] if len(c) == 9 else c for c in load_cmap(name).hex]  # strip alpha
        return cols[:n] if n else cols
    except Exception as e:
        raise KeyError(f"Unknown palette {name!r}: not in house styles, Bokeh, "
                       f"matplotlib, palettable, or pypalettes.") from e


# --- Curated recommendations for housing work (task -> good palettes) ---
CURATED = {
    "categorical_operators": ["won", "Category10", "Bold", "jchs"],
    "categorical_types":     ["Set2", "Prism", "Bold", "jchs"],
    "sequential_choropleth": ["YlOrBr", "Blues", "Thermal", "viridis", "cividis"],
    "diverging_change":      ["RdYlBu", "RdBu", "Balance", "coolwarm"],
    "report_house_styles":   ["won", "hud", "jchs", "crs"],
}
