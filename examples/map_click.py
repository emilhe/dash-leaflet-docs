import dash_html_components as html
import dash_leaflet as dl
from dash_extensions.enrich import DashProxy, Input, Output

app = DashProxy(prevent_initial_callbacks=True)
app.layout = html.Div([
    dl.Map([dl.TileLayer(), dl.LayerGroup(id="layer")],
           id="map", style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"}),
])


@app.callback(Output("layer", "children"), [Input("map", "click_lat_lng")])
def map_click(click_lat_lng):
    return [dl.Marker(position=click_lat_lng, children=dl.Tooltip("({:.3f}, {:.3f})".format(*click_lat_lng)))]


if __name__ == '__main__':
    app.run_server()
