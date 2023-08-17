import dash_leaflet as dl
from dash_extensions.enrich import DashProxy, html, Output, Input
from dash.exceptions import PreventUpdate
from dash_extensions.javascript import assign

# How to render geojson.
point_to_layer = assign("""function(feature, latlng, context){
    const p = feature.properties;
    if(p.type === 'circlemarker'){return L.circleMarker(latlng, radius=p._radius)}
    if(p.type === 'circle'){return L.circle(latlng, radius=p._mRadius)}
    return L.marker(latlng);
}""")
# Create example app.
app = DashProxy()
app.layout = html.Div([
    # Setup a map with the edit control.
    dl.Map(center=[56, 10], zoom=4, children=[
        dl.TileLayer(), dl.FeatureGroup([
            dl.EditControl(id="edit_control"), dl.Marker(position=[56, 10])]),
    ], style={'width': '50%', 'height': '50vh', 'margin': "auto", "display": "inline-block"}, id="map"),
    # Setup another map to that mirrors the edit control geometries using the GeoJSON component.
    dl.Map(center=[56, 10], zoom=4, children=[
        dl.TileLayer(), dl.GeoJSON(id="geojson", pointToLayer=point_to_layer, zoomToBounds=True),
    ], style={'width': '50%', 'height': '50vh', 'margin': "auto", "display": "inline-block"}, id="mirror"),
])

# Copy data from the edit control to the geojson component.
@app.callback(Output("geojson", "data"), Input("edit_control", "geojson"))
def mirror(x):
    if not x:
        raise PreventUpdate
    return x

if __name__ == '__main__':
    app.run_server()
