import dash
import dash_html_components as html
import dash_leaflet as dl
import requests

# Get some example data (a list of dicts with {name: country name, latlng: position tuple, ...})
marker_data = requests.get("https://gist.githubusercontent.com/erdem/8c7d26765831d0f9a8c62f02782ae00d/raw"
                           "/248037cd701af0a4957cce340dabb0fd04e38f4c/countries.json").json()
# Create marker cluster.
markers = [dl.Marker(children=dl.Tooltip(item["name"]), position=item["latlng"]) for item in marker_data]
cluster = dl.MarkerClusterGroup(id="markers", children=markers, options={"polygonOptions": {"color": "red"}})
# Create app.
app = dash.Dash()
app.layout = html.Div(dl.Map([dl.TileLayer(), cluster], zoom=3, center=(51, 10)),
                      style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"})

if __name__ == '__main__':
    app.run_server()
