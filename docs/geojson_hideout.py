import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.enrich import DashProxy, html, dcc, Output, Input
from dash_extensions.javascript import assign

# A few cities in Denmark.
cities = [dict(name="Aalborg", lat=57.0268172, lon=9.837735),
          dict(name="Aarhus", lat=56.1780842, lon=10.1119354),
          dict(name="Copenhagen", lat=55.6712474, lon=12.5237848)]
# Create drop down options.
dd_options = [dict(value=c["name"], label=c["name"]) for c in cities]
dd_defaults = [o["value"] for o in dd_options]
# Generate geojson with a marker for each city and name as tooltip.
geojson = dlx.dicts_to_geojson([{**c, **dict(tooltip=c['name'])} for c in cities])
# Create javascript function that filters on feature name.
geojson_filter = assign("function(feature, context){return context.hideout.includes(feature.properties.name);}")
# Create example app.
app = DashProxy()
app.layout = html.Div([
    dl.Map(children=[
        dl.TileLayer(),
        dl.GeoJSON(data=geojson, filter=geojson_filter, hideout=dd_defaults, id="geojson")
    ], style={'height': '50vh'}, center=[56, 10], zoom=6, id='map'),
    dcc.Dropdown(id="dd", value=dd_defaults, options=dd_options, clearable=False, multi=True)
])
# Link drop down to geojson hideout prop (could be done with a normal callback, but clientside is more performant).
app.clientside_callback("function(x){return x;}", Output("geojson", "hideout"), Input("dd", "value"))

if __name__ == '__main__':
    app.run_server()
