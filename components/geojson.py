import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.enrich import DashProxy, html, Output, Input

# Generate some in-memory data.
bermuda = dlx.dicts_to_geojson([dict(lat=32.299507, lon=-64.790337)])
# Create example app.
app = DashProxy()
app.layout = html.Div([
    dl.Map(center=[39, -98], zoom=4, children=[
        dl.TileLayer(),
        dl.GeoJSON(data=bermuda),  # in-memory geojson (slowest option)
        dl.GeoJSON(url="/assets/us-states.json", id="states"),  # geojson resource (faster than in-memory)
    ], style={'width': '100%', 'height': '50vh'}, id="map"),
    html.Div(id="state"), html.Div(id="capital")
])


@app.callback(Output("state", "children"), [Input("states", "data-click")])
def capital_click(feature):
    if feature is not None:
        return f"You clicked {feature['properties']['name']}"


if __name__ == '__main__':
    app.run_server()
