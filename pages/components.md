### Components

The majority of components are light wrappers of their React-Leaflet counterparts. For documentation on these components, the [React-Leaflet API component reference](https://react-leaflet.js.org/docs/en/components) as well as the [Leaflet API reference](https://leafletjs.com/reference.html) are great resources. For details on the Dash integration specifically, consider the component links to the left, or the [source code](https://github.com/thedirtyfew/dash-leaflet) itself.

#### Leaflet plugins

In addition to the core components, a vast amount of Leaflet plugins exists. A few on the more popular ones have been ported,

* [`PolylineDecorator`](https://github.com/bbecquet/Leaflet.PolylineDecorator)
* [`LocateControl`](https://github.com/domoritz/leaflet-locatecontrol)
* [`MeasureControl`](https://github.com/ljagis/leaflet-measure)
* [`EditControl`](https://github.com/Leaflet/Leaflet.draw)

To get a taste of what each of these component can do, the documentation of the underlying Leaflet component is a good place to start. For implementation details, e.g. which props are exposed, consult the [source code](https://github.com/thedirtyfew/dash-leaflet).

#### Custom components

A few custom component have also been developed,

* `DivMarker` (a customized marker that uses a [DivIcon](https://leafletjs.com/reference.html#divicon) instead of an [Icon](https://leafletjs.com/reference.html#icon))
* `ColorBar` (a simple color bar, typically used to with plots)
* `GeoJSON` (based on the [Leaflet GeoJSON component](https://leafletjs.com/reference-1.6.0.html#geojson) and [supercluster](https://github.com/mapbox/supercluster))

