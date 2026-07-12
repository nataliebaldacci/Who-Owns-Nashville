# chart_cookbook — index

_Auto-generated catalog of every script, grouped by category. Visual previews live in `figures/`. See `README.md` for palettes, styles, boundary helpers._


**74 Python scripts** + Chart.js gallery + style/palette/boundary modules.


## Reference / layout

- **`python/subplot_layouts.py`** — Subplot layout reference (matplotlib subplot / subplots / subplot2grid). A practical cheatsheet: a composed mini-dashboard using subplot2grid custom
- **`style_showcase.py`** — Renders the same bar, line, and stacked-bar in three house styles (WON, JCHS, CRS) so you can compare the color systems side by side.

## Ranking — who has the most

- **`python/ranking/01_barplot.py`** — Basic bar plot — RANKING Style inspired by the Python Graph Gallery (python-graph-gallery.com).
- **`python/ranking/02_horizontal_barplot.py`** — Horizontal bar plot — RANKING Best when category labels are long. Inspired by python-graph-gallery.com.
- **`python/ranking/03_lollipop.py`** — Lollipop chart — RANKING A lighter alternative to bars. Inspired by python-graph-gallery.com.
- **`python/ranking/04_cleveland_dotplot.py`** — Cleveland dot plot — RANKING (two series compared) Compares two values per category (e.g. TN vs out-of-state). Inspired by python-graph-gallery.com.
- **`python/ranking/05_dumbbell_lollipop.py`** — Dumbbell / lollipop with colormap segments + custom legend (Cedric Scherer Mario Kart style). Per operator: first-acquisition median value (grey dot) to
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
- **`python/evolution/29_line_end_labels.py`** — Line chart with labels at the end of each line (Cedric Scherer Big Mac style). Operator cumulative acquisitions over time; highlighted operators colored + end-
- **`python/evolution/30_stacked_area_inline_labels.py`** — Smoothed stacked area with inline labels (Gilbert Fontana wealth-chart style). Ownership composition over time, spline-smoothed, custom palette, big title,
- **`python/evolution/31_stacked_area_inflection_arrows.py`** — Stacked area with inline labels + inflection arrows (Joseph Barbier natural- disasters style). Ownership composition over years, custom palette, right-side

## Distribution — spread of values

- **`python/distribution/11_histogram.py`** — Histogram — DISTRIBUTION Shape of a single numeric variable. Inspired by python-graph-gallery.com.
- **`python/distribution/12_density_kde.py`** — Density (KDE) plot — DISTRIBUTION Smoothed distribution; good for comparing groups. Inspired by python-graph-gallery.com.
- **`python/distribution/13_boxplot.py`** — Box plot — DISTRIBUTION Median, quartiles, outliers across groups. Inspired by python-graph-gallery.com.
- **`python/distribution/14_violin.py`** — Violin plot — DISTRIBUTION Box plot + density silhouette. Inspired by python-graph-gallery.com.
- **`python/distribution/21_ridgeline.py`** — Ridgeline — DISTRIBUTION. Many groups' distributions stacked (price per year).
- **`python/distribution/27_ridgeline_annotated.py`** — Annotated ridgeline with quantile bands + legend inset (rent-by-adjective style, Ansgar Wolsing / Joseph Barbier). Sale-price distribution by buyer type,
- **`python/distribution/28_insee_pyramid.py`** — INSEE 'salary pyramid' style annotated histogram (Joseph Barbier translation). A horizontal histogram of Davidson home-value ranges with a per-bar color gradien

## Correlation — how variables relate

- **`python/correlation/15_scatter.py`** — Scatter plot — CORRELATION Relationship between two numeric variables. Inspired by python-graph-gallery.com.
- **`python/correlation/16_bubble.py`** — Bubble chart — CORRELATION Scatter with a third variable encoded as marker size. Inspired by python-graph-gallery.com.
- **`python/correlation/17_correlogram_heatmap.py`** — Correlogram / heatmap — CORRELATION Correlation matrix as a colored grid. Inspired by python-graph-gallery.com.
- **`python/correlation/18_annotated_bubble_quadrant.py`** — Annotated quadrant bubble plot (Datawrapper climate-risk style). Block groups by institutional rate (x) vs poverty rate (y), bubble size = residential parcels,
- **`python/correlation/19_scatter_regression_labels.py`** — Scatter with regression fit + auto-positioned labels (Claus Wilke corruption style). Block groups: income (x) vs institutional rate (y), log fit, colored by
- **`python/correlation/24_connected_scatter.py`** — Connected scatter — CORRELATION. Two variables tracked over time (path).

## Maps — geography

- **`python/map/18_choropleth.py`** — Choropleth — MAP (static, geopandas). Davidson tracts shaded by institutional %. Uses the JCHS orange sequential ramp and quantile classes (mapclassify).
- **`python/map/19_bubble_map.py`** — Bubble map — MAP (static, geopandas). County outline + one bubble per block group, sized by institutional-parcel count, colored by rate.
- **`python/map/27_folium_choropleth.py`** — Folium interactive choropleth — MAP. Davidson tracts shaded by institutional %, with hover tooltips. Writes 27_folium_choropleth.html (opens in any browser).
- **`python/map/29_bokeh_choropleth.py`** — Bokeh interactive choropleth — MAP. Adapts the Bokeh county-unemployment example (LogColorMapper + HoverTool) to Davidson tracts / institutional %.
- **`python/map/30_boundaries_overview.py`** — Boundaries overview — MAP. All Davidson boundary layers side by side, so you can see the geography options for any choropleth (census + local).
- **`python/map/31_choropleth_by_zip.py`** — Choropleth by ZIP — MAP. Spatial-joins corporate-owned parcels to ZIP codes and shades each ZIP by the count. Shows how to aggregate any point layer to any
- **`python/map/32_palette_gallery.py`** — Palette variety gallery — MAP. The SAME Davidson block-group choropleth (institutional share of single-family rentals) rendered across ~36 popular
- **`python/map/33_atlanta_style_choropleth.py`** — Atlanta-style choropleth — MAP. Replicates the dark-basemap census-tract look (percent by tract, plasma ramp, manual bins, styled legend box, scale bar) for
- **`python/map/34_folium_dark_interactive.py`** — Interactive dark choropleth — MAP. Leaflet/folium version matching the ACS maps already on the site: CartoDB dark tiles, binned plasma choropleth, and a
- **`python/map/35_choropleth_histogram.py`** — Choropleth + inset histogram (Joseph Barbier / Python Graph Gallery style). Davidson tracts shaded by institutional %, with an inset histogram that doubles
- **`python/map/36_choropleth_barplot.py`** — Choropleth + inset bar distribution (Belgium 'Sunset3' style, Koen Van den Eeckhout / Joseph Barbier). Davidson tracts shaded by institutional %, custom
- **`python/map/37_choropleth_binned_barplot.py`** — Choropleth + binned seaborn barplot legend (Sao Paulo HDI style, Vinicius Oike / Joseph Barbier). Davidson tracts shaded by institutional %; the inset horizonta
- **`python/map/38_annotated_bubble_map.py`** — Annotated bubble map (eclipse-map style, Joseph Barbier). Davidson county outline + one bubble per block group, colored by institutional rate and sized by
- **`python/map/39_choropleth_custom_legend.py`** — Choropleth with a custom rectangle legend + arrow annotation (Joseph Barbier CO2-Europe style). Davidson tracts shaded by institutional %, BrwnYl ramp, a

## Flow — volume between stages

- **`python/flow/20_sankey_plotly.py`** — Sankey diagram — FLOW Flows between stages (e.g. builder -> operator -> status). Uses Plotly.

## CRS report figures

- **`python/crs_reports/crs_new_vs_existing.py`** — CRS 'New vs Existing Homes' style: stacked bars, blue = New, orange = Existing. For Davidson: split each year's SF sales by parcel year-built vs sale year
- **`python/crs_reports/crs_starts_by_type.py`** — CRS/HUD 'Housing Starts by Type' style: stacked area, orange=SF, grey=MF for sale, gold=MF for rent, per 1,000 population.
- **`python/crs_reports/crs_total_housing_units.py`** — CRS 'Total Housing Units' style (R48892 Fig 1): tan bars for the level, blue line for the units-to-population ratio on a right axis. Dual-axis.

## Interactive (Bokeh)

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

## Composite / multi-panel

- **`python/composite/39_heatmap_radial.py`** — Heatmap + radial barcharts composite (Margaret Siple / TidyTuesday style, Python port by Tomas Capretto). A dot-heatmap of each operator's property-type
- **`python/composite/40_stacked_area_tilemap.py`** — Stacked-area small-multiples arranged as a map (Erin Davis 'viral map' style). One mini stacked-area per Davidson council district, positioned at the district
- **`python/composite/41_economist_line_area.py`** — Economist-style two-panel line + stacked area (child-labour chart style) with flexitext titles and a red top bar. Left: institutional rate over time by tier.
- **`python/composite/42_small_multiples_highlight.py`** — Small multiples with highlighted lines + annotations (Joseph Barbier unemployment style). 3x3 grid, one operator highlighted per panel over a greyed

## Styles & palettes

- **`styles/boundaries.py`** — Registry of Davidson County boundary layers available in the repo, so any cookbook map can aggregate a metric to whichever geography you need.
- **`styles/morethemes_demo.py`** — morethemes demo — the same bar chart in four report-grade themes. Run: python styles/morethemes_demo.py  ->  figures/morethemes_demo.png
- **`styles/palette_reference.py`** — Draw a browsable swatch sheet of representative palettes across every library the cookbook can reach. Run: python styles/palette_reference.py
- **`styles/palettes.py`** — Unified palette accessor for the chart cookbook.
- **`styles/won_styles.py`** — Shared house-style palettes for the chart cookbook.
- **`chartjs/index.html`** — 6 chart types rebuilt in Chart.js (HUD-style boxes).
