"""Palette variety gallery — MAP. The SAME Davidson block-group choropleth
(institutional share of single-family rentals) rendered across ~36 popular
palettes from palettable (cmocean, CARTOColors, Scientific, ColorBrewer) plus
matplotlib/seaborn. Quantile-classed (k=6) so the spatial pattern is identical
and only the color scheme differs — a pick-your-palette sheet.

Change BOUNDARY to "block" for the finest breakdown, or "tract" for coarser.
"""
import matplotlib; matplotlib.use("Agg")
import sys, os, importlib; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
import matplotlib.pyplot as plt
import geopandas as gpd

ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
SOURCE = {
    "block":      ("institutional_by_block.geojson",      "rate"),
    "blockgroup": ("institutional_by_blockgroup.geojson", "rate"),
    "tract":      ("Davidson_Institutional_Pct_by_Tract.geojson", "pct_institutional"),
}
BOUNDARY = "blockgroup"
fname, col = SOURCE[BOUNDARY]
gdf = gpd.read_file(os.path.join(ROOT, fname))
gdf = gdf[gdf[col].notna()]

# (label, kind, spec) — kind: pal=palettable family.Name, mpl, sns
PALETTES = [
    # ColorBrewer sequential
    ("cb: YlOrBr", "pal", "colorbrewer.sequential.YlOrBr_9"),
    ("cb: YlGnBu", "pal", "colorbrewer.sequential.YlGnBu_9"),
    ("cb: BuPu",   "pal", "colorbrewer.sequential.BuPu_9"),
    ("cb: PuBuGn", "pal", "colorbrewer.sequential.PuBuGn_9"),
    # cmocean sequential
    ("cmo: Thermal", "pal", "cmocean.sequential.Thermal_20"),
    ("cmo: Haline",  "pal", "cmocean.sequential.Haline_20"),
    ("cmo: Matter",  "pal", "cmocean.sequential.Matter_20"),
    ("cmo: Dense",   "pal", "cmocean.sequential.Dense_20"),
    ("cmo: Deep",    "pal", "cmocean.sequential.Deep_20"),
    ("cmo: Tempo",   "pal", "cmocean.sequential.Tempo_20"),
    ("cmo: Amp",     "pal", "cmocean.sequential.Amp_20"),
    ("cmo: Ice",     "pal", "cmocean.sequential.Ice_20"),
    # CARTOColors sequential
    ("carto: SunsetDark", "pal", "cartocolors.sequential.SunsetDark_7"),
    ("carto: Sunset",     "pal", "cartocolors.sequential.Sunset_7"),
    ("carto: Magenta",    "pal", "cartocolors.sequential.Magenta_7"),
    ("carto: Teal",       "pal", "cartocolors.sequential.Teal_7"),
    ("carto: BluYl",      "pal", "cartocolors.sequential.BluYl_7"),
    ("carto: PurpOr",     "pal", "cartocolors.sequential.PurpOr_7"),
    ("carto: Emrld",      "pal", "cartocolors.sequential.Emrld_7"),
    ("carto: DarkMint",   "pal", "cartocolors.sequential.DarkMint_7"),
    # Scientific (Crameri) sequential
    ("sci: Batlow", "pal", "scientific.sequential.Batlow_20"),
    ("sci: Bilbao", "pal", "scientific.sequential.Bilbao_20"),
    ("sci: LaJolla","pal", "scientific.sequential.LaJolla_20"),
    ("sci: Davos",  "pal", "scientific.sequential.Davos_20"),
    ("sci: Oslo",   "pal", "scientific.sequential.Oslo_20"),
    ("sci: Turku",  "pal", "scientific.sequential.Turku_20"),
    # matplotlib / seaborn
    ("mpl: viridis", "mpl", "viridis"),
    ("mpl: magma",   "mpl", "magma"),
    ("mpl: inferno", "mpl", "inferno"),
    ("mpl: plasma",  "mpl", "plasma"),
    ("mpl: cividis", "mpl", "cividis"),
    ("sns: rocket",  "sns", "rocket"),
    ("sns: mako",    "sns", "mako"),
    ("sns: flare",   "sns", "flare"),
    ("sns: crest",   "sns", "crest"),
    ("sns: icefire", "sns", "icefire"),
]


def cmap_of(kind, spec):
    if kind == "mpl":
        return plt.get_cmap(spec)
    if kind == "sns":
        import seaborn as sns
        return sns.color_palette(spec, as_cmap=True)
    fam, name = spec.rsplit(".", 1)
    mod = importlib.import_module("palettable." + fam)
    return getattr(mod, name).mpl_colormap


cols = 6
rows = (len(PALETTES) + cols - 1) // cols
fig, axes = plt.subplots(rows, cols, figsize=(cols * 3.0, rows * 2.7))
for ax, (label, kind, spec) in zip(axes.flat, PALETTES):
    try:
        cm = cmap_of(kind, spec)
        gdf.plot(column=col, cmap=cm, scheme="quantiles", k=6, linewidth=0.05,
                 edgecolor="white", ax=ax)
    except Exception as e:
        ax.text(0.5, 0.5, f"skip\n{label}", ha="center", va="center", fontsize=7)
    ax.set_title(label, fontsize=9); ax.axis("off")
for ax in axes.flat[len(PALETTES):]:
    ax.axis("off")
fig.suptitle(f"Palette variety — institutional share of single-family rentals by "
             f"{BOUNDARY} (quantile classes, identical breaks)\n"
             f"palettable: ColorBrewer · cmocean · CARTOColors · Scientific  +  matplotlib/seaborn",
             fontsize=13, fontweight="bold")
plt.tight_layout(rect=[0, 0, 1, .96])
plt.savefig("32_palette_gallery.png", dpi=115)
print(f"wrote 32_palette_gallery.png — {len(PALETTES)} palettes on {len(gdf)} {BOUNDARY} features")
