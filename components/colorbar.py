import dash_leaflet as dl
from dash_extensions.enrich import DashProxy

colorscale = ['red', 'yellow', 'green', 'blue', 'purple']  # rainbow
app = DashProxy()
app.layout = dl.Map([
    dl.TileLayer(),
    dl.Colorbar(colorscale=colorscale, width=20, height=200, min=0, max=50, position="topright")
], center=[56, 10], zoom=6,  style={'height': '50vh'})

if __name__ == "__main__":
    app.run_server()