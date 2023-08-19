import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.enrich import DashProxy, html

app = DashProxy()
app.layout = html.Div([
    dl.Map([
        dl.TileLayer(),
        # From in-memory geojson. All markers at same point forces spiderfy at any zoom level.
        dl.GeoJSON(data=dlx.dicts_to_geojson([dict(lat=-37.8, lon=175.6)] * 100), cluster=True),
        # From hosted asset (best performance).
        dl.GeoJSON(url='assets/leaflet_50k.pbf', format="geobuf", cluster=True, id="sc", zoomToBoundsOnClick=True,
                   superClusterOptions={"radius": 100}),
    ], center=(-37.75, 175.4), zoom=11, style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"}),
])

if __name__ == '__main__':
    app.run_server()
