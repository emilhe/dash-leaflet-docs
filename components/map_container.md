## MapContainer

The `MapContainer` component (aliased `Map` for brevity and backwards compatibility) is the root container for the `dash-leaflet` component tree. It supports a ton of options, and exposes a [huge number of events](https://leafletjs.com/reference.html#map-event) (for information on how to access them, see the [Events](/docs/events) page). 

.. dash-proxy:: components.map_container

### Manipulating the viewport

Since map options are [immutable](/docs/getting_started#a-property-mutability), it is not possible to manipulate the viewport of the `MapContainer` after initialization via the `zoom`/`center`/`bounds` properties. To enable viewport manipulation from Dash, a special `viewport` property has been added. Here is a small example, where the `zoom`/`center` is changed using the `flyTo` transition,

.. dash-proxy:: components.map_container_fly_to

### Getting on Click and maps bounds / zoom position
This example demonstrates how to capture click events on the map and track the map's current center and zoom level using Dash-Leaflet. Here's what the code does:

1. Click Events: The map_click callback listens for the clickData event on the map. When a user clicks on the map, it places a marker at the clicked location and displays the coordinates.
2. Map Center and Zoom: The update_center callback uses the map's bounds and zoom properties to calculate and display the current center coordinates and zoom level of the map view.
3. Dynamic Updates: As the user interacts with the map (panning, zooming, or clicking), the displayed information updates in real-time.
4. Error Handling: The code includes error handling to manage potential issues with data processing, ensuring robustness.

This setup allows for creating interactive maps where users can both place markers and see the current map view details, useful for various mapping applications.

.. dash-proxy:: components.map_container_onclick_center

.. api-doc:: dash_leaflet.MapContainer