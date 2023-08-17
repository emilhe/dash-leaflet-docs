import dash_leaflet as dl
from dash_extensions.enrich import DashProxy, html
from dash_extensions.javascript import arrow_function

# Create geojson.
geojson = dl.GeoJSON(url="/assets/us-states.json", zoomToBounds=True,
                     hoverStyle=arrow_function(dict(weight=5, color='#666', dashArray='')))
# Create app.
app = DashProxy()
app.layout = dl.Map(children=[dl.TileLayer(), geojson], style={'height': '50vh'})

if __name__ == '__main__':
    app.run_server()