import json

import dash_leaflet as dl
from dash_extensions.enrich import DashProxy, Input, Output, html
from dash_extensions.javascript import assign

# Send data back to Dash.
event_handlers = dict(measurefinish=assign("function(e, ctx){ctx.setProps({measureData: {area: e.area}})}"))
# Create small example app.
app = DashProxy()
app.layout = html.Div(
    [
        dl.Map(
            [
                dl.TileLayer(),
                dl.MeasureControl(position="topleft", primaryLengthUnit="kilometers", primaryAreaUnit="hectares"),
            ],
            eventHandlers=event_handlers,
            center=[56, 10],
            zoom=6,
            style={"height": "50vh"},
            id="map",
        ),
        html.Div(id="log"),
    ]
)


@app.callback(Output("log", "children"), Input("map", "measureData"))
def log(data):
    return json.dumps(data)


if __name__ == "__main__":
    app.run()
