import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.enrich import DashProxy, html, Output, Input

# Generate some in-memory data, and add a simply popup with the name.
bermuda = dlx.dicts_to_geojson([dict(lat=32.299507, lon=-64.790337, popup="Bermuda")])
# Create example app.
app = DashProxy()
app.layout = html.Div([
    dl.Map(center=[39, -98], zoom=4, children=[
        dl.TileLayer(),
        dl.GeoJSON(data=bermuda),  # in-memory geojson (slowest option)
        dl.GeoJSON(url="/assets/us-states.json", id="states"),  # geojson resource (faster than in-memory)
    ], style={'height': '50vh'}),
    html.Div(id="state")
])


@app.callback(Output("state", "children"), [Input("states", "clickData")])
def state_click(feature):
    if feature is not None:
        return f"You clicked {feature['properties']['name']}"


if __name__ == '__main__':
    app.run_server()
