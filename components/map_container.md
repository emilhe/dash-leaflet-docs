## MapContainer

The `MapContainer` component (aliased `Map` for brevity and backwards compatibility) is the root container for the `dash-leaflet` component tree. It supports a ton of options, and exposes a [huge number of events](https://leafletjs.com/reference.html#map-event) (for information on how to access them, see the [Events](/docs/events) page). 

.. dash-proxy:: components.map_container

### Manipulating the viewport

Since map options are [immutable](/docs/getting_started#a-property-mutability), it is not possible to manipulate the viewport of the `MapContainer` after initialization via the `zoom`/`center`/`bounds` properties. To enable viewport manipulation from Dash, a special `viewport` property has been added. Here is a small example, where the `zoom`/`center` is changed using the `flyTo` transition,

.. dash-proxy:: components.map_container_fly_to

.. api-doc:: dash_leaflet.MapContainer