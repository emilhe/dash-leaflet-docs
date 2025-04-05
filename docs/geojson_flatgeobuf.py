import dash_leaflet as dl
from dash_extensions.enrich import DashProxy, Input, Output, html
from dash_extensions.javascript import arrow_function


def get_rect(center: list[float], delta: float = 2):
    return dict(minX=center[1] - delta, maxX=center[1] + delta, minY=center[0] - delta, maxY=center[0] + delta)


initial_center = [39, -98]
app = DashProxy()
app.layout = html.Div(
    [
        dl.Map(
            center=initial_center,
            zoom=6,
            children=[
                dl.TileLayer(),
                dl.GeoJSON(
                    url="/assets/us-counties.fgb",
                    format="flatgeobuf",
                    id="counties",
                    formatOptions=dict(rect=get_rect(initial_center)),  # only load data within this rectangle
                    hoverStyle=arrow_function(dict(weight=5, color="#666", dashArray="")),
                ),
            ],
            style={"height": "50vh"},
            id="map",
        ),
    ]
)


@app.callback(Output("counties", "formatOptions"), [Input("map", "clickData")], prevent_initial_call=True)
def load_counties(click_data):
    new_center = [click_data["latlng"]["lat"], click_data["latlng"]["lng"]]
    return dict(rect=get_rect(new_center))


if __name__ == "__main__":
    app.run(port=8889)  # , debug=True)
