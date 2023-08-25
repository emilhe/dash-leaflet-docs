import dash_leaflet as dl
from dash_extensions.enrich import DashProxy

# Custom icon as per official docs https://leafletjs.com/examples/custom-icons/
custom_icon = dict(
    iconUrl='https://leafletjs.com/examples/custom-icons/leaf-green.png',
    shadowUrl='https://leafletjs.com/examples/custom-icons/leaf-shadow.png',
    iconSize=[38, 95],
    shadowSize=[50, 64],
    iconAnchor=[22, 94],
    shadowAnchor=[4, 62],
    popupAnchor=[-3, -76]
)
# Small example app.
app = DashProxy()
app.layout = dl.Map([
    dl.TileLayer(),
    dl.Marker(position=[55, 10]),
    dl.Marker(position=[57, 10], icon=custom_icon),
], center=[56, 10], zoom=6, style={'height': '50vh'})

if __name__ == '__main__':
    app.run_server()
