## GeoJSON

The `GeoJSON` component enables visualization of geospatial data. It is wrapper of [Leaflet GeoJSON component](https://leafletjs.com/reference.html#geojson), but with a significant amount of functionality added on top, including built-in marker clustering using the [supercluster library](https://github.com/mapbox/supercluster) and async loading of data from static assets. Properties of type `Function` can be passed by supplying the [full path to the function](/docs/func_props). The use of functional properties makes the `GeoJSON` component both performant and extremely customizable. Below is a very simple example, but many more are available in the [`GeoJSON` tutorial](/docs/geojson_tutorial).

.. dash-proxy:: components.geojson

.. api-doc:: dash_leaflet.GeoJSON