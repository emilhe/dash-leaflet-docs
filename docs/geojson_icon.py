import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.enrich import DashProxy, html
from dash_extensions.javascript import assign

# A few countries.
countries = [dict(name="Denmark", iso2="dk", lat=56.26392, lon=9.501785),
             dict(name="Sweden", iso2="se", lat=59.334591, lon=18.063240),
             dict(name="Norway", iso2="no", lat=59.911491, lon=9.501785)]
# Generate geojson with a marker for each country and name as tooltip.
geojson = dlx.dicts_to_geojson([{**c, **dict(tooltip=c['name'])} for c in countries])
# Create javascript function th at draws a marker with a custom icon, in this case a flag hosted by flagcdn.
draw_flag = assign("""function(feature, latlng){
const flag = L.icon({iconUrl: `https://flagcdn.com/64x48/${feature.properties.iso2}.png`, iconSize: [64, 48]});
return L.marker(latlng, {icon: flag});
}""")
# Create example app.
app = DashProxy()
app.layout = html.Div([
    dl.Map(children=[
        dl.TileLayer(), dl.GeoJSON(data=geojson, pointToLayer=draw_flag, zoomToBounds=True)
    ], style={'height': '50vh'}, center=[56, 10], zoom=6)
])

if __name__ == '__main__':
    app.run()