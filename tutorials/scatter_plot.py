import dash_leaflet as dl
import dash_leaflet.express as dlx
import pandas as pd
from dash_extensions.javascript import assign
from dash_extensions.enrich import DashProxy, html

colorscale = ['red', 'yellow', 'green', 'blue', 'purple']  # rainbow
chroma = "https://cdnjs.cloudflare.com/ajax/libs/chroma-js/2.1.0/chroma.min.js"  # js lib used for colors
color_prop = 'density'
# Pre process the data into geobuf.
df = pd.read_csv("assets/uscities.csv")  # data from https://simplemaps.com/data/us-cities
df = df[df['state_name'] == 'Washington']  # select one state
df = df[['lat', 'lng', 'city', color_prop]]  # drop irrelevant columns
dicts = df.to_dict('rows')
for item in dicts:
    item["tooltip"] = "{} ({:.1f})".format(item['city'], item[color_prop])  # bind tooltip
geojson = dlx.dicts_to_geojson(dicts, lon="lng")  # convert to geojson
geobuf = dlx.geojson_to_geobuf(geojson)  # convert to geobuf
# Create a colorbar.
vmax = df[color_prop].max()
colorbar = dl.Colorbar(colorscale=colorscale, width=20, height=150, min=0, max=vmax, unit='/km2')
# Geojson rendering logic, must be JavaScript as it is executed in clientside.
point_to_layer = assign("""function(feature, latlng, context){
    const {min, max, colorscale, circleOptions, colorProp} = context.props.hideout;
    const csc = chroma.scale(colorscale).domain([min, max]);  // chroma lib to construct colorscale
    circleOptions.fillColor = csc(feature.properties[colorProp]);  // set color based on color prop.
    return L.circleMarker(latlng, circleOptions);  // sender a simple circle marker.
}""")
# Create geojson.
geojson = dl.GeoJSON(data=geobuf, id="geojson", format="geobuf",
                     zoomToBounds=True,  # when true, zooms to bounds when data changes
                     options=dict(pointToLayer=point_to_layer),  # how to draw points
                     superClusterOptions=dict(radius=50),   # adjust cluster size
                     hideout=dict(colorProp=color_prop, circleOptions=dict(fillOpacity=1, stroke=False, radius=5),
                                  min=0, max=vmax, colorscale=colorscale))
# Create the app.
app = DashProxy(external_scripts=[chroma], prevent_initial_callbacks=True)
app.layout = html.Div([
    dl.Map([dl.TileLayer(), geojson, colorbar]),
], style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block", "position": "relative"})

if __name__ == '__main__':
    app.run_server()
