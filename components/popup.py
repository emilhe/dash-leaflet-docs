import dash_leaflet as dl
from dash_extensions.enrich import DashProxy, html

center = [56, 10]
app = DashProxy()
app.layout = dl.Map([
    dl.TileLayer(),
    dl.Popup(position=[57, 10], children="Hello world!"),
    dl.Marker(position=[55, 10], children=[dl.Popup(content="This is <b>html<b/>!")])
], center=center, zoom=6, style={'width': '100%', 'height': '50vh'})


if __name__ == '__main__':
    app.run_server()
