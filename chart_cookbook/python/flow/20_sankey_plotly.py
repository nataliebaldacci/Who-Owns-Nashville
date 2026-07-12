"""
Sankey diagram — FLOW
Flows between stages (e.g. builder -> operator -> status). Uses Plotly.
Inspired by python-graph-gallery.com. Writes an interactive HTML + a PNG
(PNG export needs `kaleido`: pip install kaleido).
"""
import plotly.graph_objects as go

labels = ["Builder", "Progress", "AMH", "Amherst",
          "Rental", "Exited", "Pipeline"]
# source/target are indices into `labels`
src = [0, 0, 0, 1, 1, 2, 2, 3, 3]
tgt = [1, 2, 3, 4, 5, 4, 6, 4, 5]
val = [1215, 1182, 699, 900, 200, 850, 150, 500, 120]

fig = go.Figure(go.Sankey(
    node=dict(label=labels, pad=18, thickness=16,
              color=["#8a94a0", "#e6194b", "#2166ac", "#1a9850",
                     "#1c458c", "#d7263d", "#f0af1e"]),
    link=dict(source=src, target=tgt, value=val,
              color="rgba(28,69,140,0.25)"),
))
fig.update_layout(title_text="Parcel Flow: Builder → Operator → Status", font_size=12)
fig.write_html("20_sankey_plotly.html")
try:
    fig.write_image("20_sankey_plotly.png", width=900, height=520, scale=2)
except Exception as e:
    print("PNG export skipped (install kaleido):", e)
