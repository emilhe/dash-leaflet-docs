from dash_extensions.javascript import assign
from dash_extensions.enrich import DashProxy
from dash_leaflet import Map, TileLayer

eventHandlers = dict(
    contextmenu=assign("function(e, ctx){ctx.map.flyTo([13.87992, 45.9791], 12);}"),
)
app = DashProxy(__name__)
app.layout = Map(children=[TileLayer()], eventHandlers=eventHandlers,
                 style={'height': '50vh'}, center=[56, 10], zoom=6)

if __name__ == '__main__':
    app.run_server()
