import dash_leaflet as dl
import dash_leaflet.express as dlx
import pandas as pd
from dash_extensions.javascript import assign
from dash_extensions.enrich import DashProxy, html

colorscale = ['red', 'yellow', 'green', 'blue', 'purple']  # rainbow
chroma = "https://cdnjs.cloudflare.com/ajax/libs/chroma-js/2.1.0/chroma.min.js"  # js lib used for colors
color_prop = 'density'
# Create a colorbar.
vmin = 0
vmax = 1000
colorbar = dl.Colorbar(colorscale=colorscale, width=20, height=150, min=vmin, max=vmax, unit='/km2')
# Geojson rendering logic, must be JavaScript as it is executed in clientside.
on_each_feature = assign("""function(feature, layer, context){
    if(feature.properties.city){  // don't bind anything for clusters (that do not have a city prop)
        layer.bindTooltip(`${feature.properties.city} (${feature.properties.density})`)
    }
}""")
point_to_layer = assign("""function(feature, latlng, context){
    const {min, max, colorscale, circleOptions, colorProp} = context.hideout;
    const csc = chroma.scale(colorscale).domain([min, max]);  // chroma lib to construct colorscale
    circleOptions.fillColor = csc(feature.properties[colorProp]);  // set color based on color prop
    return L.circleMarker(latlng, circleOptions);  // render a simple circle marker
}""")
cluster_to_layer = assign("""function(feature, latlng, index, context){
    const {min, max, colorscale, circleOptions, colorProp} = context.hideout;
    const csc = chroma.scale(colorscale).domain([min, max]);
    // Set color based on mean value of leaves.
    const leaves = index.getLeaves(feature.properties.cluster_id);
    let valueSum = 0;
    for (let i = 0; i < leaves.length; ++i) {
        valueSum += leaves[i].properties[colorProp]
    }
    const valueMean = valueSum / leaves.length;
    // Modify icon background color.
    const scatterIcon = L.DivIcon.extend({
        createIcon: function(oldIcon) {
               let icon = L.DivIcon.prototype.createIcon.call(this, oldIcon);
               icon.style.backgroundColor = this.options.color;
               return icon;
        }
    })
    // Render a circle with the number of leaves written in the center.
    const icon = new scatterIcon({
        html: '<div style="background-color:white;"><span>' + feature.properties.point_count_abbreviated + '</span></div>',
        className: "marker-cluster",
        iconSize: L.point(40, 40),
        color: csc(valueMean)
    });
    return L.marker(latlng, {icon : icon})
}""")
# Create geojson.
geojson = dl.GeoJSON(url="/assets/us-cities.json",
                     cluster=True,  # when true, data are clustered
                     zoomToBounds=True,  # when true, zooms to bounds when data changes
                     pointToLayer=point_to_layer,  # how to draw points
                     onEachFeature=on_each_feature,  # add (custom) tooltip
                     clusterToLayer=cluster_to_layer,  # how to draw clusters
                     zoomToBoundsOnClick=True,  # when true, zooms to bounds of feature (e.g. cluster) on click
                     superClusterOptions=dict(radius=150),   # adjust cluster size
                     hideout=dict(colorProp=color_prop, circleOptions=dict(fillOpacity=1, stroke=False, radius=5),
                                  min=vmin, max=vmax, colorscale=colorscale))
# Create the app.
app = DashProxy(external_scripts=[chroma], prevent_initial_callbacks=True)
app.layout = dl.Map([dl.TileLayer(), geojson, colorbar], center=[56, 10], zoom=6, style={'height': '50vh'})

if __name__ == '__main__':
    app.run_server()
