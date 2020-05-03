## Components

The majority of components are light wrappers of their React-Leaflet counterparts. For now, the following components (besides `Map`) have been ported,

* UI Layers
    * `Marker`
    * `Popup`
    * `Tooltip`
* Raster Layers
    * `TileLayer`
    * `WMSTileLayer`
    * `ImageOverlay`
    * `VideoOverlay`
* Vector Layers
    * `Circle`
    * `CircleMarker`
    * `Polyline`
    * `Polygon`
    * `Rectangle`
    * `SVGOverlay`
* Other Layers
    * `LayerGroup`
    * `GeoJSON`
* Controls
    * `ScaleControl`


For documentation on these components, the [React-Leaflet API component reference](https://react-leaflet.js.org/docs/en/components) is a great resource. For additional details, consider the [source code](https://github.com/thedirtyfew/dash-leaflet).

##### Leaflet plugins

In addition to the core components, a vast amount of Leaflet plugins exists. A few on the more popular ones have been ported,

* [`MarkerClusterGroup`](https://github.com/Leaflet/Leaflet.markercluster)
* [`LocateControl`](https://github.com/domoritz/leaflet-locatecontrol)
* `GeoTIFFOverlay` (custom component)

To get a taste of what each of these component can do, the documentation of the underlying Leaflet component is a good place to start. For implementation details, e.g. which props are exposed, consult the [source code](https://github.com/thedirtyfew/dash-leaflet).
