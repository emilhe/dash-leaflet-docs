from dash_extensions.enrich import DashProxy
import dash_leaflet as dl

app = DashProxy()
app.layout = dl.Map([
    dl.TileLayer(),
    dl.Pane(dl.Marker(position=[56, 9]), style=dict(zIndex=501), name="upper"),
    dl.Pane(dl.Rectangle(bounds=[[55, 9], [57, 10]], fillOpacity=1), style=dict(zIndex=500), name="middle"),
    dl.Pane(dl.Marker(position=[56, 10]), style=dict(zIndex=499), name="lower")
], center=[56, 10], zoom=6, style={'height': '50vh'})

if __name__ == '__main__':
    app.run()