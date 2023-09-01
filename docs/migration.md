## Migration

This pages contains migration guidelines for releases that contain breaking changes.

### 1.0.0

In the 1.0.0 release of `dash-leaflet`, the library was completely rewritten based on React Leaflet v4 (previous versions of `dash-leaflet` were based on React Leaflet v2). As part of this process, a few components were dropped,

- `Minichart`: The underlying library is not maintained, and the current version in incompatible with newer versions of Leaflet
- `MarkerClusterGroup`: Performance was poor for large numbers (> 100) of markers. The `GeoJSON` component provides superior performance (with clustering enabled, > 1 million markers is supported)
- `GeoTIFFOverlay`: This (highly custom) component has long been deprecated, and I decided now was the time to drop it

In addition, a number of breaking changes were introduced,

- `Map`: The `center/zoom` (or `bounds`) props are now mandatory. If not provided, the map will be blank
- `Map`: The `location_lat_lon_acc` prop has been dropped
- `Map`: The `click_lat_lng/dbl_click_lat_lng` prop have been dropped in favor of `clickData`/`dblclickData`
- `GeoJSON`: The structure of the context passed to user-defined functions has changed. Previously, to access `myProp` the code would be `context.props.myProp`, now it is just `context.myProp` (similar to event contexts)
- `GeoJSON`: The name of the event data props has changed from `click_feature`/`hover_feature` to `clickData`/`hoverData` (similar to other event data props)
- `GestureHandling`: Options no longer supported due to a bug in current version of the underlying component
- `VideoOverlay`: The `click_lat_lng/dbl_click_lat_lng` prop have been dropped in favor of `clickData`/`dblclickData`
- `Polygon`: The `click_lat_lng/dbl_click_lat_lng` prop have been dropped in favor of `clickData`/`dblclickData`
- `Polyline`: The `click_lat_lng/dbl_click_lat_lng` prop have been dropped in favor of `clickData`/`dblclickData`
- `Rectangle`: The `click_lat_lng/dbl_click_lat_lng` prop have been dropped in favor of `clickData`/`dblclickData`
- `ImageOverlay`: The `click_lat_lng/dbl_click_lat_lng` prop have been dropped in favor of `clickData`/`dblclickData`
- `ImageOverlay`: The `loaded` prop have been dropped in favor of `loadData`

Along with a number of non-breaking changes, including but not limited to,

- `Map`: The name of the root container has changed from `Map` to `MapContainer` to match the React Leaflet conventions. However, a `Map` alias has been added to enable backwards compatibility
- `GeoJSON`: Previously options to the `GeoJSON` component were passed via the `options` prop, now they are set directly. However, for backwards compatibility any options passed via the `options` prop are passed on to the component
