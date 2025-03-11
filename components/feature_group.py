import dash_leaflet as dl
from dash_extensions.enrich import DashProxy
from dash_extensions.javascript import assign

app = DashProxy()
app.layout = dl.Map([
    dl.TileLayer(),
    dl.FeatureGroup([
        dl.Marker(position=[56, 10]),
        dl.Marker(position=[56, 12]),
    ], eventHandlers=dict(
        contextmenu=assign("function(e){alert('Marker right click!')}")
    ))
], center=[56, 10], zoom=6, style={'height': '50vh'})

if __name__ == '__main__':
    app.run()
