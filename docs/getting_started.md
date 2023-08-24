## Installation

The preferred way to install `dash-leaflet` is via pip,

```bash
pip install dash-leaflet
```

or, if you are using [Poetry](https://python-poetry.org),

```bash
poetry add dash-leaflet
```

### Example

It should now be possible to run the following (minimal) example app,

.. dash-proxy:: docs.minimal

### Optional dependencies

Other recommended/related packages include

* [`dash-extensions`](https://www.dash-extensions.com/) for supercharged Dash development
* [`dash-mantine-components`](https://www.dash-mantine-components.com/) for creating user interfaces in Dash

This documentation is itself a Dash app created using `dash-mantine-components`, `dash-extensions`, [`dash-iconify`](https://www.dash-mantine-components.com/getting-started/dash-iconify), and [`dash-down`](https://github.com/emilhe/dash-down).

## Property mutability

The `dash-leaflet` libray is built on top of the [React Leaflet library](https://react-leaflet.js.org/), which is itself built on the [Leaflet library](https://leafletjs.com/). The React Leaflet library introduces the concept of [_mutable_ and _immutable_ properties](https://react-leaflet.js.org/docs/api-components/). Mutable properties can be changed after a component has been constructed (e.g. in Dash via a callback), while immutable cannot. If you find yourself in need of changing an immutable property, you should instead recreate the component with the immutable prop(s) set accordingly. 

### Property tags

Mutable properties are marked in the docstring by a `[MUTABLE]` tag. One such example is the `zoomToBoundsOnClick` property of the `GeoJSON` component,

    - zoomToBoundsOnClick (boolean; optional):
        If True, zoom to feature bounds on click. [MUTABLE, DL].

This particular property is also marked by the `[DL]` tag, which indicates that the property was created and/or tailored as part of `dash-leaflet`. Hence, documentation may not be available in the underlying libraries and/or the behavior in `dash-leaflet` may deviate from what is documented there.

## Component uniqueness

It should be noted that components with the same id are considered "the same". If you try to re-create a component while assigning it the same id, React may attempt to update the old component instead of creating a new one(!). Hence, unless you only change mutable properties (for which updates are possible) in the process, the old component property values may stick around, causing unintended behavior. Here is a small example,

.. dash-proxy:: docs.component_uniqueness

## Component overview

All components are documented in the `dash-leaflet` component API reference (available in the left menubar on desktop, or via the searchbar on mobile devices). The documentation for each component consists of (1) a short, explanatory text followed by an interactive demo along with the necessary code to run it as a standalone app, and (2) an outline of the component keyword arguments.

### React Leaflet

The majority of components are light wrappers of their React Leaflet counterparts,

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
    * `FeatureGroup`
    * `Pane`
* Controls
    * `ZoomControl`
    * `AttributionControl`
    * `LayersControl`
    * `ScaleControl`

For documentation on these components, the [React-Leaflet API component reference](https://react-leaflet.js.org/docs/api-components/) as well as the [Leaflet API reference](https://leafletjs.com/reference.html) are great resources. 

### Leaflet plugins

In addition to the core components, a vast amount of Leaflet plugins exists. A few on the more popular ones have been ported,

* [`PolylineDecorator`](https://github.com/bbecquet/Leaflet.PolylineDecorator)
* [`LocateControl`](https://github.com/domoritz/leaflet-locatecontrol)
* [`MeasureControl`](https://github.com/ljagis/leaflet-measure)
* [`EditControl`](https://github.com/Leaflet/Leaflet.draw)
* [`EasyButton`](https://github.com/CliffCloud/Leaflet.EasyButton)
* [`FullScreenControl`](https://github.com/brunob/leaflet.fullscreen)
* [`GestureHandling`](https://github.com/brunob/leaflet.fullscreen)


To get a taste of what each of these component can do, the documentation of the underlying Leaflet component is a good place to start.

### Custom components

A few custom component have also been developed,

* `DivMarker` (a customized marker that uses a [DivIcon](https://leafletjs.com/reference.html#divicon) instead of an [Icon](https://leafletjs.com/reference.html#icon))
* `ColorBar` (a simple color bar, typically used to with plots)
* `GeoJSON` (based on the [Leaflet GeoJSON component](https://leafletjs.com/reference-1.6.0.html#geojson) and [supercluster](https://github.com/mapbox/supercluster))

In general, the documentation for these components is limited `dash-leaflet` component API reference, and the [source code](https://github.com/thedirtyfew/dash-leaflet) itself. In case of the (rather complex) `GeoJSON` component, a [dedicated tutorial](/docs/geojson_tutorial) is available.