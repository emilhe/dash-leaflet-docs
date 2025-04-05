import dash_leaflet as dl
from dash_extensions.enrich import DashProxy

# Cool, dark tiles by Stadia Maps.
url = "https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png"
attribution = '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a> '
# Create app.
app = DashProxy()
app.layout = dl.Map(
    [dl.TileLayer(url=url, maxZoom=20, attribution=attribution)], center=[56, 10], zoom=6, style={"height": "50vh"}
)

if __name__ == "__main__":
    app.run()
