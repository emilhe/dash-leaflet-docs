from dash_extensions.enrich import DashProxy
import dash_leaflet as dl

app = DashProxy()
app.layout = dl.Map([
    dl.TileLayer(),
    dl.Polygon(positions=[[57, 10], [57, 11], [56, 11]])
], center=[56, 10], zoom=6, style={'width': '100%', 'height': '50vh'})

if __name__ == '__main__':
    app.run_server()