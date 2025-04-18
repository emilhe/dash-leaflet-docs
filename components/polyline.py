import dash_leaflet as dl
from dash_extensions.enrich import DashProxy

app = DashProxy()
app.layout = dl.Map(
    [dl.TileLayer(), dl.Polyline(positions=[[57, 10], [57, 11], [56, 11]])],
    center=[56, 10],
    zoom=6,
    style={"height": "50vh"},
)

if __name__ == "__main__":
    app.run()
