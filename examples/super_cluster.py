import dash
import dash_html_components as html
import dash_leaflet as dl
import dash_leaflet.express as dlx
import json

from dash.dependencies import Input, Output

# Create a few customized markers.
custom_markers = [
    dict(lat=-37.8, lon=174.95, tooltip="I am a tooltip"),  # marker with tooltip
    dict(lat=-37.8, lon=175.00, popup="I am a popup"),  # marker with popup
    dict(lat=-37.8, lon=175.05, markerOptions=dict(opacity=0.5)),  # marker with options
    dict(lat=-37.8, lon=175.10, markerOptions=dict(icon=dict(iconUrl="assets/icon_plane.png"))),  # custom icon
]
# Create a few markers a the same location to illustrate spiderfy.
spider_markers = [dict(lat=-37.8, lon=175.6)] * 100
# Create example app.
app = dash.Dash()
app.layout = html.Div([
    dl.Map([
        dl.TileLayer(),
        # From in-memory geojson.
        dl.SuperCluster(data=dlx.markers_to_geojson(custom_markers)),
        # Using dlx convenience wrapper. Sends data as base64 encoded geobuf, smaller payload than geojson.
        dlx.supercluster(spider_markers),
        # From hosted asset (best performance).
        dl.SuperCluster(url='assets/leaflet_50k.pbf', format="geobuf", superclusterOptions={"radius": 100}, id="sc"),
    ], center=(-37.8, 175.3), zoom=11, style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"}),
    # Logging element.
    html.Div(id="log")
])


@app.callback(Output("log", "children"), [Input("sc", "featureClick"), Input("sc", "featureHover")])
def log(click, hover):
    return json.dumps([click, hover])


if __name__ == '__main__':
    app.run_server()
