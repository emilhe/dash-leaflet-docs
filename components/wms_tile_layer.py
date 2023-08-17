import dash_leaflet as dl
from dash_extensions.enrich import DashProxy

app = DashProxy()
app.layout = dl.Map([
    dl.TileLayer(), dl.WMSTileLayer(url="https://mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0r.cgi",
                                            layers="nexrad-n0r-900913", format="image/png", transparent=True)
], center=[40, -100], zoom=4, style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"})

if __name__ == '__main__':
    app.run_server()
