## GeoJSON tutorial

The purpose of the `GeoJSON` tutorial is to illustrate the flexibility of the `GeoJSON` component. Before diving into the tutorial, it might be beneficial to read the section on [functional properties](/docs/func_props).

### Marker clustering

The GeoJSON component supports marker clustering using the [supercluster library](https://github.com/mapbox/supercluster). It can be enabled by passing `cluster=True`. Other options include `zoomToBoundsOnClick` (zoom to cluster on click) and `spiderfyOnMaxZoom` (draw markers in a spider formation if they can't be resolved at max zoom). Options to supercluster can be passed via the `superClusterOptions` property. The cluster symbol can be modified via the `clusterToLayer` property.

.. dash-proxy:: docs.super_cluster

### Feature filtering

The `filter` property of the `GeoJSON` component makes it possible to show only a subset of the features contained in a geojson resource. In the example below, all markers except the one labeled `Aarhus` is filtered out.

.. dash-proxy:: docs.geojson_filter

### Interactivity via the hideout prop

The standard approach to achieve interactivity in Dash is to replace a component by a new component with modified properties. While this approach works for the `GeoJSON` component too, performance may be poor for large datasets. A more efficient way to achieve interactivity is to render the `GeoJSON` data conditionally based on the content of the `hideout` property. By doing so, interactivity can then be achieved by changing the `hideout` prop from Dash (through callbacks). Note that by default the `hideout` prop does nothing, its sole purpose is to act as a proxy for passing state from Dash to the `GeoJSON` component.

In the example below, the filter example is made interactive using this approach. Notice how fast the map reacts to the dropdown selection changes. That's because everything happens clientside. This pattern can be applied to achieve performant interactivity in many other use cases too, e.g. changing the symbol of a marker or the color of a polygon.  

.. dash-proxy:: docs.geojson_hideout
   :prefix: geojson_hideout

### Highlighting a selected feature

There are many ways realise highlighting of a selected feature. In this example, we'll be using _conditional rendering_. Hence, we create a function that renders features in different ways, depending on whether then are selected or not. Similar to the previous example, the `hideout` property is used to store _state_, in this case which features are currently selected. To enable interactivity, the `hideout` property must be updated when the selection changes. In this example, a callback is added to toggle the selection on click.

.. dash-proxy:: docs.geojson_select
   :prefix: geojson_select

The selection toggling could also be implemented as a clientside callback, which would yield a better performance,

    ...
    toggle_select = """function(_, feature, hideout){
        let selected = hideout.selected;
        const name = feature.properties.name;
        if(selected.includes(name)){selected = selected.filter((item) => (item !== name))}
        else{selected.push(name);}
        return {selected: selected};
    }"""
    app.clientside_callback(toggle_select,
                            Output("geojson", "hideout"),
                            Input("geojson", "n_clicks"),
                            State("geojson", "clickData"),
                            State("geojson", "hideout"),
                            prevent_initial_call=True)
    ...

### Custom icons

It is possible to use any marker icon with the `GeoJSON` component. Simply add the icon to the assets directory and set the url accordingly, or use a hosted icon. The example below demonstrates how to draw different icons for different features based on the feature properties.

.. dash-proxy:: docs.geojson_icon

### Scatter Plot

The `GeoJSON` component supports customization of how points are rendered via the `pointToLayer` option. In this example, a scatter plot is created by rendering the points as circle markers colored based on a feature value (population density). Note that since the colorscale is constructed using the `chroma` javascript library, it must be pass via the `external_scripts` keyword of the `Dash` object.

.. dash-proxy:: docs.scatter_plot

### Scatter Cluster

Just like the `pointToLayer` prop controls point rendered, the `clusterToLayer` prop controls how clustered are rendered. In the example below, the scatter plot example is extended to perform clustering with a custom cluster rendering function that draws a colored circle (with the color based on the average value of the clustered points) with the number of clustered points printed in the center.

.. dash-proxy:: docs.scatter_cluster


### Choropleth Map

The `style` option of the `GeoJSON` component controls how polygons are rendered. By configuring it properly, it is possible to create choropleth visualizations. The example below is essentially a reproduction of the [interactive choropleth map](https://leafletjs.com/examples/choropleth/) in the Leaflet example gallery. 

.. dash-proxy:: docs.choropleth_us
   :prefix: choropleth_us

A bit of CSS was used to style the info box,

    .info {
        padding: 6px 8px;
        font: 14px/16px Arial, Helvetica, sans-serif;
        background: white;
        background: rgba(255,255,255,0.8);
        box-shadow: 0 0 15px rgba(0,0,0,0.2);
        border-radius: 5px;
    }
    .info h4 {
        margin: 0 0 5px;
        color: #777;
    }