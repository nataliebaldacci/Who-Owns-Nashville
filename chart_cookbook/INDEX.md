# chart_cookbook — index

_Auto-generated catalog of every script, grouped by category. Visual previews live in `figures/`. See `README.md` for palettes, styles, boundary helpers._


**91 Python scripts** + Chart.js gallery + style/palette/boundary modules.


## Reference / layout

- **`python/subplot_layouts.py`** — Subplot layout reference (matplotlib subplot / subplots / subplot2grid). A practical cheatsheet: a composed mini-dashboard using subplot2grid custom proportions, plus the layout re
- **`style_showcase.py`** — Renders the same bar, line, and stacked-bar in three house styles (WON, JCHS, CRS) so you can compare the color systems side by side.

## Ranking — who has the most

- **`python/ranking/01_barplot.py`** — Basic bar plot — RANKING Style inspired by the Python Graph Gallery (python-graph-gallery.com). Swap the sample DataFrame for your own (e.g. owner_leaderboard.json).
- **`python/ranking/02_horizontal_barplot.py`** — Horizontal bar plot — RANKING Best when category labels are long. Inspired by python-graph-gallery.com.
- **`python/ranking/03_lollipop.py`** — Lollipop chart — RANKING A lighter alternative to bars. Inspired by python-graph-gallery.com.
- **`python/ranking/04_cleveland_dotplot.py`** — Cleveland dot plot — RANKING (two series compared) Compares two values per category (e.g. TN vs out-of-state). Inspired by python-graph-gallery.com.
- **`python/ranking/05_dumbbell_lollipop.py`** — Dumbbell / lollipop with colormap segments + custom legend (Cedric Scherer Mario Kart style). Per operator: first-acquisition median value (grey dot) to latest median value (blue d
- **`python/ranking/06_economist_hbar.py`** — Horizontal barplot in The Economist "Escape artists" style. Blue bars, value labels placed inside (white) or outside (blue, path-effect stroke) depending on bar length, top x-axis 
- **`python/ranking/22_radar.py`** — Radar / spider — RANKING. One or two entities across several metrics.

## Part of whole — how the total splits

- **`python/part_of_whole/05_stacked_barplot.py`** — Stacked bar plot — PART OF WHOLE Composition within each category. Inspired by python-graph-gallery.com.
- **`python/part_of_whole/06_treemap.py`** — Treemap — PART OF WHOLE Nested rectangles sized by value. Needs `squarify`. Inspired by python-graph-gallery.com.
- **`python/part_of_whole/07_donut.py`** — Donut chart — PART OF WHOLE Use sparingly (few categories). Inspired by python-graph-gallery.com.
- **`python/part_of_whole/23_waffle.py`** — Waffle — PART OF WHOLE. Share of a total as a 10x10 grid of squares.

## Evolution — change over time

- **`python/evolution/08_line.py`** — Line chart — EVOLUTION A value over time. Inspired by python-graph-gallery.com.
- **`python/evolution/09_area.py`** — Area chart — EVOLUTION Line with filled area to emphasize magnitude. Inspired by python-graph-gallery.com.
- **`python/evolution/10_stacked_area.py`** — Stacked area chart — EVOLUTION Composition over time. Inspired by python-graph-gallery.com.
- **`python/evolution/25_streamgraph.py`** — Streamgraph — EVOLUTION. Stacked area with a wiggle baseline (flowing).
- **`python/evolution/26_timeseries.py`** — Timeseries — EVOLUTION. Proper datetime x-axis with monthly data.
- **`python/evolution/29_line_end_labels.py`** — Line chart with labels at the end of each line (Cedric Scherer Big Mac style). Operator cumulative acquisitions over time; highlighted operators colored + end- labeled with leader 
- **`python/evolution/30_stacked_area_inline_labels.py`** — Smoothed stacked area with inline labels (Gilbert Fontana wealth-chart style). Ownership composition over time, spline-smoothed, custom palette, big title, year total callouts, and
- **`python/evolution/31_stacked_area_inflection_arrows.py`** — Stacked area with inline labels + inflection arrows (Joseph Barbier natural- disasters style). Ownership composition over years, custom palette, right-side inline labels, and drawa
- **`python/evolution/32_small_multiples_lines.py`** — Small multiples for a line chart (python-graph-gallery anti-spaghetti style). A 3x3 grid, one panel per owner, each panel drawing every owner's acquisition curve in faint grey with
- **`python/evolution/33_minimalist_area.py`** — Minimalist two-color area chart (Joseph Barbier "Japan population" style). One line + filled area, split into a green segment (positive) and a red segment (negative) around a zero 
- **`python/evolution/34_animated_stacked_area.py`** — Animated stacked-area chart with text that highlights key events (Joseph Barbier "space objects" style). A GIF that grows a two-band stacked area of the cumulative corporate SFR fo
- **`python/evolution/35_percent_stacked_area.py`** — Percent (100%) stacked area chart (python-graph-gallery style). Each year's values are normalized to sum to 100%, so the chart reads as a changing MIX rather than a growing total. 
- **`python/evolution/36_streamgraph_customized.py`** — Customized streamgraph — colors, order and smoothing (python-graph-gallery X-Men "mutant moneyball" style). Demonstrates the full customization workflow on a streamgraph: (1) color

## Distribution — spread of one variable

- **`python/distribution/11_histogram.py`** — Histogram — DISTRIBUTION Shape of a single numeric variable. Inspired by python-graph-gallery.com.
- **`python/distribution/12_density_kde.py`** — Density (KDE) plot — DISTRIBUTION Smoothed distribution; good for comparing groups. Inspired by python-graph-gallery.com.
- **`python/distribution/13_boxplot.py`** — Box plot — DISTRIBUTION Median, quartiles, outliers across groups. Inspired by python-graph-gallery.com.
- **`python/distribution/14_violin.py`** — Violin plot — DISTRIBUTION Box plot + density silhouette. Inspired by python-graph-gallery.com.
- **`python/distribution/21_ridgeline.py`** — Ridgeline — DISTRIBUTION. Many groups' distributions stacked (price per year).
- **`python/distribution/27_ridgeline_annotated.py`** — Annotated ridgeline with quantile bands + legend inset (rent-by-adjective style, Ansgar Wolsing / Joseph Barbier). Sale-price distribution by buyer type, each row filled by quantil
- **`python/distribution/28_insee_pyramid.py`** — INSEE 'salary pyramid' style annotated histogram (Joseph Barbier translation). A horizontal histogram of Davidson home-value ranges with a per-bar color gradient, title/subtitle/cr
- **`python/distribution/30_mirror_density_histogram.py`** — Mirror density + histogram (python-graph-gallery style): compare two distributions back-to-back around a zero baseline. Real data — corporate SFR acquisitions in Davidson County by

## Correlation — how variables relate

- **`python/correlation/15_scatter.py`** — Scatter plot — CORRELATION Relationship between two numeric variables. Inspired by python-graph-gallery.com.
- **`python/correlation/16_bubble.py`** — Bubble chart — CORRELATION Scatter with a third variable encoded as marker size. Inspired by python-graph-gallery.com.
- **`python/correlation/17_correlogram_heatmap.py`** — Correlogram / heatmap — CORRELATION Correlation matrix as a colored grid. Inspired by python-graph-gallery.com.
- **`python/correlation/18_annotated_bubble_quadrant.py`** — Annotated quadrant bubble plot (Datawrapper climate-risk style). Block groups by institutional rate (x) vs poverty rate (y), bubble size = residential parcels, quadrant reference l
- **`python/correlation/19_scatter_regression_labels.py`** — Scatter with regression fit + auto-positioned labels (Claus Wilke corruption style). Block groups: income (x) vs institutional rate (y), log fit, colored by poverty tercile, extrem
- **`python/correlation/20_custom_legends.py`** — Custom legends in Matplotlib — a reference sheet (python-graph-gallery style). Six panels of the same scatter (corporate parcel size vs year built, colored by property type) each s
- **`python/correlation/21_bubble_4d.py`** — Four-dimensional bubble plot (gapminder style, matplotlib + seaborn). One point per Davidson block group encoding four variables at once: x = poverty rate, y = median household inc
- **`python/correlation/24_connected_scatter.py`** — Connected scatter — CORRELATION. Two variables tracked over time (path).

## Map — where, geographically

- **`python/map/18_choropleth.py`** — Choropleth — MAP (static, geopandas). Davidson tracts shaded by institutional %. Uses the JCHS orange sequential ramp and quantile classes (mapclassify).
- **`python/map/19_bubble_map.py`** — Bubble map — MAP (static, geopandas). County outline + one bubble per block group, sized by institutional-parcel count, colored by rate.
- **`python/map/27_folium_choropleth.py`** — Folium interactive choropleth — MAP. Davidson tracts shaded by institutional %, with hover tooltips. Writes 27_folium_choropleth.html (opens in any browser).
- **`python/map/29_bokeh_choropleth.py`** — Bokeh interactive choropleth — MAP. Adapts the Bokeh county-unemployment example (LogColorMapper + HoverTool) to Davidson tracts / institutional %. Self-contained HTML via INLINE r
- **`python/map/30_boundaries_overview.py`** — Boundaries overview — MAP. All Davidson boundary layers side by side, so you can see the geography options for any choropleth (census + local).
- **`python/map/31_choropleth_by_zip.py`** — Choropleth by ZIP — MAP. Spatial-joins corporate-owned parcels to ZIP codes and shades each ZIP by the count. Shows how to aggregate any point layer to any boundary via styles.boun
- **`python/map/32_palette_gallery.py`** — Palette variety gallery — MAP. The SAME Davidson block-group choropleth (institutional share of single-family rentals) rendered across ~36 popular palettes from palettable (cmocean
- **`python/map/33_atlanta_style_choropleth.py`** — Atlanta-style choropleth — MAP. Replicates the dark-basemap census-tract look (percent by tract, plasma ramp, manual bins, styled legend box, scale bar) for Davidson County. Option
- **`python/map/34_folium_dark_interactive.py`** — Interactive dark choropleth — MAP. Leaflet/folium version matching the ACS maps already on the site: CartoDB dark tiles, binned plasma choropleth, and a hover tooltip per tract. Wr
- **`python/map/35_choropleth_histogram.py`** — Choropleth + inset histogram (Joseph Barbier / Python Graph Gallery style). Davidson tracts shaded by institutional %, with an inset histogram that doubles as the legend (bars colo
- **`python/map/36_choropleth_barplot.py`** — Choropleth + inset bar distribution (Belgium 'Sunset3' style, Koen Van den Eeckhout / Joseph Barbier). Davidson tracts shaded by institutional %, custom create_cmap palette, inset 
- **`python/map/37_choropleth_binned_barplot.py`** — Choropleth + binned seaborn barplot legend (Sao Paulo HDI style, Vinicius Oike / Joseph Barbier). Davidson tracts shaded by institutional %; the inset horizontal barplot bins the m
- **`python/map/38_annotated_bubble_map.py`** — Annotated bubble map (eclipse-map style, Joseph Barbier). Davidson county outline + one bubble per block group, colored by institutional rate and sized by count, with a highlight_t
- **`python/map/39_choropleth_custom_legend.py`** — Choropleth with a custom rectangle legend + arrow annotation (Joseph Barbier CO2-Europe style). Davidson tracts shaded by institutional %, BrwnYl ramp, a hand-built swatch legend, 
- **`python/map/40_geoplot_polyplot.py`** — Draw a map straight from a GeoJSON with GeoPandas + GeoPlot (python-graph- gallery "polyplot" style). Loads a Davidson boundary layer into a GeoDataFrame and draws the polygons wit
- **`python/map/41_geoplot_choropleth.py`** — Choropleth map with GeoPandas + GeoPlot (python-graph-gallery style). Loads a Davidson GeoJSON, uses a mapclassify Quantiles(k) binning scheme, and draws the choropleth with gplt.c
- **`python/map/42_plotly_choropleth.py`** — Interactive choropleth with Plotly Express (python-graph-gallery style). Loads a Davidson GeoJSON, colors each census tract by institutional ownership rate with px.choropleth_map, 
- **`python/map/43_basemap_bubble.py`** — Bubble map with Basemap (python-graph-gallery style). Basemap draws the background (county extent, land fill, coastline-style boundary) and matplotlib scatters one orange bubble pe
- **`python/map/45_basemap_bubble_categorical.py`** — Categorical bubble map with Basemap (python-graph-gallery surf-tweets style). Basemap draws the background; matplotlib scatters one bubble per block group, sized by institutional p

## Flow — volume between stages

- **`python/flow/20_sankey_plotly.py`** — Sankey diagram — FLOW Flows between stages (e.g. builder -> operator -> status). Uses Plotly. Inspired by python-graph-gallery.com. Writes an interactive HTML + a PNG (PNG export n

## Composite / annotated multi-panel

- **`python/composite/39_heatmap_radial.py`** — Heatmap + radial barcharts composite (Margaret Siple / TidyTuesday style, Python port by Tomas Capretto). A dot-heatmap of each operator's property-type mix, plus radial barplots f
- **`python/composite/40_stacked_area_tilemap.py`** — Stacked-area small-multiples arranged as a map (Erin Davis 'viral map' style). One mini stacked-area per Davidson council district, positioned at the district centroid, showing own
- **`python/composite/41_economist_line_area.py`** — Economist-style two-panel line + stacked area (child-labour chart style) with flexitext titles and a red top bar. Left: institutional rate over time by tier. Right: parcel counts b
- **`python/composite/42_small_multiples_highlight.py`** — Small multiples with highlighted lines + annotations (Joseph Barbier unemployment style). 3x3 grid, one operator highlighted per panel over a greyed backdrop of all others, with fi
- **`python/composite/43_bump_small_multiples.py`** — Multi-panel highlighted bump/ranking lineplots (Abdoul Madjid water-rankings style). One panel per operator; each highlights that operator's RANK trajectory (by parcels acquired pe
- **`python/composite/44_multi_choropleth_lollipop.py`** — Multiple choropleth maps with a lollipop plot for the legend (Joseph Barbier "happiness in Europe" style). Four small block-group choropleths on a dark background, each a different

## Tables

- **`python/table/01_plottable_operators.py`** — Publication-ready table with plottable (Fortune Uwha liveability-table style). Top Davidson operators with color-coded circled metric cells (per-column colormap), grouped columns, 
- **`python/table/02_plottable_images.py`** — Publication table with logos, in the plottable "add images in a column" style (Joseph Barbier / python-graph-gallery). Each operator row carries a circular badge in an Image column
- **`python/table/03_plottable_incell_plots.py`** — Plottable table with in-cell graphs (python-graph-gallery "insert graphs in cells" chapter). Columns render mini-plots inside their cells: a progress donut and proportional bars wi
- **`python/table/04_great_tables.py`** — Table with great_tables (python-graph-gallery great_tables chapter). The gt- inspired API builds a titled, footnoted, cell-highlighted table and exports it as a self-contained HTML

## Bokeh — interactive

- **`python/bokeh/_shared.py`** — Shared Nashville sample data + save helper for the Bokeh cookbook scripts.
- **`python/bokeh/b01_dodged_bars.py`** — Dodged bar chart (Bokeh) — TN vs out-of-state holdings side by side per operator.
- **`python/bokeh/b02_stacked_bars.py`** — Stacked bar chart (Bokeh) — TN + out-of-state stacked per operator.
- **`python/bokeh/b03_grouped_nested.py`** — Grouped/nested bar chart (Bokeh) — parcels by tier then operator, factor_cmap + hover.
- **`python/bokeh/b04_crosstab_hbar.py`** — Crosstab adjacent hbar (Bokeh) — owner-type composition within each investor tier.
- **`python/bokeh/b05_line_legend_title.py`** — Multi-line time series with a styled legend title (Bokeh).
- **`python/bokeh/b06_legend_mute.py`** — Interactive muted legend (Bokeh) — click a legend entry to mute that line.
- **`python/bokeh/b07_glyph_hover.py`** — Scatter with hover highlight (Bokeh) — sale price vs living area.
- **`python/bokeh/b08_markers.py`** — Scatter marker gallery (Bokeh) — the available marker glyph types.
- **`python/bokeh/b09_linear_cmap_colorbar.py`** — Scatter with linear color mapping + colorbar (Bokeh) — parcels colored by value.
- **`python/bokeh/b10_color_mappers.py`** — Linear vs log color mapping grid (Bokeh).
- **`python/bokeh/b11_logplot.py`** — Log-axis plot (Bokeh) — growth functions on a log y-axis with a legend.
- **`python/bokeh/b12_slope.py`** — Scatter with a Slope regression line annotation (Bokeh).
- **`python/bokeh/b13_tile_map.py`** — Basemap tiles (Bokeh) — CartoDB Positron behind operator points (web mercator). Tiles load from CDN; renders in a browser like the site's Leaflet maps.
- **`python/bokeh/b14_latex_distribution.py`** — Histogram + PDF with LaTeX/mathtext axis labels (Bokeh) — sale-price distribution.
- **`python/bokeh/b15_selection_histogram.py`** — Selection histogram (Bokeh demo.bokeh.org/selection_histogram, standalone). A central scatter with a marginal histogram above (x) and to the right (y). Each histogram shows the ful

## CRS report figures

- **`python/crs_reports/crs_new_vs_existing.py`** — CRS 'New vs Existing Homes' style: stacked bars, blue = New, orange = Existing. For Davidson: split each year's SF sales by parcel year-built vs sale year (new = built within ~1-2 
- **`python/crs_reports/crs_starts_by_type.py`** — CRS/HUD 'Housing Starts by Type' style: stacked area, orange=SF, grey=MF for sale, gold=MF for rent, per 1,000 population.
- **`python/crs_reports/crs_total_housing_units.py`** — CRS 'Total Housing Units' style (R48892 Fig 1): tan bars for the level, blue line for the units-to-population ratio on a right axis. Dual-axis. Swap the sample series for Davidson 
