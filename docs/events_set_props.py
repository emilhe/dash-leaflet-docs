from dash_extensions.enrich import DashProxy, Input, Output, html
from dash_extensions.javascript import assign
from dash_leaflet import Map, TileLayer

eventHandlers = dict(dblclick=assign("function(e, ctx){ctx.setProps({data: 'Hello world!'})}"))
app = DashProxy()
app.layout = html.Div(
    [
        Map(
            children=[TileLayer()],
            eventHandlers=eventHandlers,
            style={"height": "50vh"},
            center=[56, 10],
            zoom=6,
            id="map",
        ),
        html.Div(id="log"),
    ]
)


@app.callback(Output("log", "children"), Input("map", "data"))
def log(message):
    return message


if __name__ == "__main__":
    app.run()
