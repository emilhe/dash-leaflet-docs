Scatter plots can be created using the `GeoJSON` component. The `scatter` object in the `express` module provides a few standard scatter rendering functions, e.g. coloring of a point based on the value of a feature property, but you can also [implement your own](#func_props). The example also covers a few other common patterns,

* Creating geojson data (markers) from a pandas dataframe
* Customization of the cluster rendering via the `clusterToLayer` prop (the cluster color is calculated based on the average value across the leaves)
* Binding tooltips and popups by setting the `tooltip` and `popup` the properties of the feature
* Modifying the clustering behavior via the `superClusterOptions` prop (specifically, increasing the cluster radius)
* Interactively changing the colormap (i.e. the marker rending) by modifying the `hideout` prop in a callback
* Interactively changing the data via modification of the `data` prop