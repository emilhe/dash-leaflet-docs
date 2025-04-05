import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.enrich import DashProxy, Input, Output, html
from dash_extensions.javascript import arrow_function

# Generate some in-memory data, and add a simple popup with the name.
bermuda = dlx.dicts_to_geojson([dict(lat=32.299507, lon=-64.790337, popup="Bermuda")])
bahamas = dlx.geojson_to_geobuf(dlx.dicts_to_geojson([dict(lat=24.55, lon=-78, popup="Bahamas")]))
# Create example app.
app = DashProxy()
app.layout = html.Div(
    [
        dl.Map(
            center=[39, -98],
            zoom=4,
            children=[
                dl.TileLayer(),
                dl.GeoJSON(data=bermuda),  # in-memory geojson (slowest option)
                dl.GeoJSON(data=bahamas, format="geobuf"),  # in-memory geobuf (smaller payload than geojson)
                dl.GeoJSON(
                    url="/assets/us-state-capitals.json", id="capitals"
                ),  # geojson resource (faster than in-memory)
                dl.GeoJSON(
                    url="/assets/us-states.pbf",
                    format="geobuf",
                    id="states",
                    hoverStyle=arrow_function(dict(weight=5, color="#666", dashArray="")),
                ),  # geobuf resource (fastest option)
            ],
            style={"height": "50vh"},
        ),
        html.Div(id="capital"),
    ]
)


@app.callback(Output("capital", "children"), [Input("capitals", "clickData")])
def capital_click(feature):
    if feature is not None:
        return f"You clicked {feature['properties']['name']}"


if __name__ == "__main__":
    app.run(port=7777)
