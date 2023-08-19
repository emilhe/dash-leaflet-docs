import dash_leaflet as dl
import random
from dash_extensions.enrich import DashProxy, Output, Input, html

app = DashProxy()
app.layout = html.Div([
    dl.Map([
        dl.TileLayer(),
        dl.LayerGroup(id="markers")
    ], center=[56, 10], zoom=6, style={'width': '100%', 'height': '50vh'}),
    html.Button("Generate markers", id="btn")
])

@app.callback(Output("markers", "children"), Input("btn", "n_clicks"))
def generate_markers(_):
    return [dl.Marker(position=[56 + random.random(), 10 + random.random()]) for i in range(5)]


if __name__ == '__main__':
    app.run_server()
