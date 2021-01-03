import dash_html_components as html
import dash_leaflet as dl
from dash_extensions.enrich import DashProxy

# Cool, dark tiles by Stadia Maps.
url = 'https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png'
attribution = '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a> '
# Create app.
app = DashProxy()
app.layout = html.Div([
    dl.Map(dl.TileLayer(url=url, maxZoom=20, attribution=attribution))
], style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block", "position": "relative"})

if __name__ == '__main__':
    app.run_server()
