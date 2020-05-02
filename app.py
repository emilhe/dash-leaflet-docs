import dash
import dash_html_components as html
import dash_leaflet as dl

# Create marker cluster.
marker_data = {"a": (56, 10), "b": (56, 11), "c": (55, 10), "d": (55, 11)}
markers = [dl.Marker(title=key, position=marker_data[key]) for key in marker_data]
cluster = dl.MarkerClusterGroup(id="markers", children=markers)
# Create app.
app = dash.Dash(external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
app.layout = html.Div([
    dl.Map(children=[dl.TileLayer(url="https://a.tile.openstreetmap.org/{z}/{x}/{y}.png"), cluster],
           style={'width': "100%", 'height': "100%"}, center=[55.5, 10.5], zoom=8, id="map", maxZoom=20),
], style={"position": "relative", 'width': '1000px', 'height': '500px'})


if __name__ == '__main__':
    app.run_server(debug=True)
