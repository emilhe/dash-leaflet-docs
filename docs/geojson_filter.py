import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.enrich import DashProxy, html
from dash_extensions.javascript import assign

# A few cities in Denmark.
cities = [
    dict(name="Aalborg", lat=57.0268172, lon=9.837735),
    dict(name="Aarhus", lat=56.1780842, lon=10.1119354),
    dict(name="Copenhagen", lat=55.6712474, lon=12.5237848),
]
# Generate geojson with a marker for each city and name as tooltip.
geojson = dlx.dicts_to_geojson([{**c, **dict(tooltip=c["name"])} for c in cities])
# Create javascript function that filters out all cities but Aarhus.
geojson_filter = assign("function(feature, context){{return ['Aarhus'].includes(feature.properties.name);}}")
# Create example app.
app = DashProxy()
app.layout = html.Div(
    [
        dl.Map(
            children=[dl.TileLayer(), dl.GeoJSON(data=geojson, filter=geojson_filter)],
            style={"height": "50vh"},
            center=[56, 10],
            zoom=6,
        ),
    ]
)

if __name__ == "__main__":
    app.run()
