import random
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.enrich import DashProxy
from dash_extensions.javascript import assign

# Create some markers.
points = [dict(lat=55.5 + random.random(), lon=9.5 + random.random(), value=random.random()) for i in range(100)]
data = dlx.dicts_to_geojson(points)
# Create geojson.
point_to_layer = assign("function(feature, latlng, context) {return L.circleMarker(latlng);}")
geojson = dl.GeoJSON(data=data, pointToLayer=point_to_layer)
# Create the app.
app = DashProxy()
app.layout = dl.Map([dl.TileLayer(), geojson], center=(56, 10), zoom=8, style={'height': '50vh'})

if __name__ == '__main__':
    app.run()