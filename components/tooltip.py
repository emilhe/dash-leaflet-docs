import dash_leaflet as dl
from dash_extensions.enrich import DashProxy

center = [56, 10]
app = DashProxy()
app.layout = dl.Map([
    dl.TileLayer(),
    # dl.Tooltip(position=[57, 10], children="Hello world!"),
    dl.Marker(position=[55, 10], children=[dl.Tooltip(content="This is <b>html<b/>!")])
], center=center, zoom=6, style={'height': '50vh'})


if __name__ == '__main__':
    app.run_server()
