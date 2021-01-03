import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_leaflet as dl
from dash_extensions.enrich import DashProxy
from dash.dependencies import Input, Output, State, ALL

app = DashProxy(prevent_initial_callbacks=True)
app.layout = html.Div([
    dl.Map([dl.TileLayer(), dl.LayerGroup(id="drawing"), dl.LayerGroup([], id="polygons")],
           id="map", style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"}),
    dcc.Store(id="store", data=[])
])


@app.callback([Output("store", "data"), Output("drawing", "children"), Output("polygons", "children")],
              [Input("map", "click_lat_lng"), Input({'role': 'marker', 'index': ALL}, "n_clicks")],
              [State("store", "data"), State("polygons", "children")])
def map_click(click_lat_lng, n_clicks, data, polygons):
    trigger = dash.callback_context.triggered[0]["prop_id"]
    # The map was clicked, add a new point.
    if trigger.split(".")[1] == "click_lat_lng":
        data.append(click_lat_lng)
        markers = [dl.CircleMarker(center=pos, id={'role': 'marker', 'index': i}) for i, pos in enumerate(data)]
        polyline = dl.Polyline(positions=data)
        drawing = markers + [polyline]
    # A marker was clicked, close the polygon and reset drawing.
    else:
        polygons.append(dl.Polygon(positions=data))
        data, drawing = [], []
    return data, drawing, polygons


if __name__ == '__main__':
    app.run_server()
