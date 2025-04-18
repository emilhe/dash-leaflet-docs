import dash_leaflet as dl
from dash_extensions.enrich import DashProxy

center = [56, 10]
app = DashProxy()
app.layout = dl.Map(
    [dl.TileLayer(), dl.Circle(center=center, radius=10000)], center=center, zoom=6, style={"height": "50vh"}
)


if __name__ == "__main__":
    app.run()
