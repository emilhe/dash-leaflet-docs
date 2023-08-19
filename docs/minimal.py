from dash_extensions.enrich import DashProxy
import dash_leaflet as dl

app = DashProxy()
app.layout = dl.Map(dl.TileLayer(), center=[56,10], zoom=6, style={'height': '50vh'})

if __name__ == '__main__':
    app.run_server()