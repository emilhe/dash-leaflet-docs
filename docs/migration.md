## Migration

This pages contains migration guidelines for releases that contain breaking changes.

### 1.0.0

In the 1.0.0 release of `dash-leaflet`, the library was completely rewritten based on React Leaflet v4 (previous versions of `dash-leaflet` were based on React Leaflet v2). As part of this process, a few components were dropped,

- `Minichart`: The underlying library is not maintained, and the current version in incompatible with newer versions of Leaflet
- `MarkerClusterGroup`: Performance was poor for large numbers (> 100) of markers. The `GeoJSON` component provides superior performance (with clustering enabled, > 1 million markers is supported)
- `GeoTIFFOverlay`: This (highly custom) component has long been deprecated, and I decided now was the time to drop it completely

ADD MORE STUFF HERE