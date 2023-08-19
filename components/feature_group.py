import dash_leaflet as dl
from dash_extensions.enrich import DashProxy
from dash_extensions.javascript import assign

event_handlers = dict(
    contextmenu=assign("function(e){alert('Marker right click!')}")
)
app = DashProxy()
app.layout = dl.Map([
    dl.TileLayer(),
    dl.FeatureGroup([
        dl.Marker(position=[56, 10]),
        dl.Marker(position=[56, 12]),
    ], eventHandlers=event_handlers)
], center=[56, 10], zoom=6, style={'width': '100%', 'height': '50vh'})

if __name__ == '__main__':
    app.run_server()
