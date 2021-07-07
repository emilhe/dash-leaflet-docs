import dash_leaflet as dl
from dash_extensions.enrich import DashProxy

app = DashProxy()
app.layout = dl.Map([dl.TileLayer(), dl.GestureHandling()],
                    style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"})

if __name__ == '__main__':
    app.run_server()
