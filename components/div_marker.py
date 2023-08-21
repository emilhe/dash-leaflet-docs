import dash_leaflet as dl
from dash_extensions.enrich import DashProxy

# Create marker cluster icon.
external_css = "https://unpkg.com/leaflet.markercluster@1.4.1/dist/MarkerCluster.Default.css"
icon = dict(
    html='<div><span> 10 </span></div>',
    className='marker-cluster marker-cluster-small',
    iconSize=[40, 40]
)
# Setup small example app.
app = DashProxy(external_stylesheets=[external_css])
app.layout = dl.Map([
    dl.TileLayer(),
    dl.DivMarker(position=[56, 10], iconOptions=icon)
], center=[56, 10], zoom=6, style={'height': '50vh'})

if __name__ == "__main__":
    app.run_server()
