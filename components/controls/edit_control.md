## EditControl

The `EditControl` makes it possible to draw and edit vectors and markers. It is powered by [Leaflet.draw](https://github.com/Leaflet/Leaflet.draw), but with a custom Dash integration that exposes the visible geometries in geojson format via a `geojson` property and the edit actions via an `action` property. Furthermore, an interface has been implemented to trigger button actions from Dash. Note that the EditControl must be wrapped in a `FeatureGroup`; shapes will be drawn to this component.

.. dash-proxy:: components.edit_control

.. api-doc:: dash_leaflet.EditControl