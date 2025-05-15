import dash
import dash_leaflet as dl
from dash_extensions.enrich import DashProxy, html, Output, Input


app = DashProxy()

# Initial map center coordinates and zoom level
initial_center = [51.5074, -0.1278]  # London
initial_zoom = 10

app.layout = html.Div([
    dl.Map(
        [
            dl.TileLayer(),
            dl.LayerGroup(id="layer"),
        ],
        center=initial_center,
        zoom=initial_zoom,
        id="map",
        style={'width': '100%', 'height': '50vh'}
    ),
    html.Div(id="click-coord-output"),
    html.Div(id="map-center-output")
])

@app.callback(
    Output("layer", "children"),
    Output("click-coord-output", "children"),
    Input("map", "clickData"),
)
def map_click(click_data):
    if click_data is None:
        return None, "Click on the map to place a marker"

    try:
        lat = click_data['latlng']['lat']
        lon = click_data['latlng']['lng']
        marker = dl.Marker(
            position=[lat, lon],
            children=dl.Tooltip(f"Chosen 🗺 Location: ({lat:.5f}, {lon:.5f})"),
            id="click_marker",
        )
        return [marker], f"Marker placed at: Lat {lat:.5f}, Lon {lon:.5f}"
    except KeyError as e:
        print(f"KeyError in map_click: {e}")
        print(f"click_data: {click_data}")
        return None, "Error processing click data"

def calculate_center(bounds):
    lat_center = (bounds[0][0] + bounds[1][0]) / 2
    lon_center = (bounds[0][1] + bounds[1][1]) / 2
    return [lat_center, lon_center]

@app.callback(
    Output("map-center-output", "children"),
    Input("map", "bounds"),
    Input("map", "zoom"),
)
def update_center(bounds, zoom):
    if not bounds or zoom is None:
        return "Map center: Not available"
    try:
        center = calculate_center(bounds)
        return f"Map center: Lat {center[0]:.5f}, Lon {center[1]:.5f}, Zoom: {zoom:.1f}"
    except Exception as e:
        print(f"Error in update_center: {e}")
        print(f"bounds: {bounds}, zoom: {zoom}")
        return "Map center: Error in data format"

if __name__ == '__main__':
    app.run_server()