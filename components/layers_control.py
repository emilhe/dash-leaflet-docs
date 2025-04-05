import json

import dash_leaflet as dl
from dash_extensions.enrich import DashProxy, Input, Output, html

# Some shapes.
markers = [dl.Marker(position=[56, 10]), dl.CircleMarker(center=[55, 10], radius=50)]
polygon = dl.Polygon(positions=[[57, 10], [57, 11], [56, 11], [57, 10]])
# Some tile urls.
keys = ["toner", "terrain"]
url_template = "http://{{s}}.tile.stamen.com/{}/{{z}}/{{x}}/{{y}}.png"
attribution = (
    'Map tiles by <a href="http://stamen.com">Stamen Design</a>, '
    '<a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data '
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
)
# Create app.
app = DashProxy()
app.layout = html.Div(
    [
        dl.Map(
            [
                dl.LayersControl(
                    [
                        dl.BaseLayer(
                            dl.TileLayer(url=url_template.format(key), attribution=attribution),
                            name=key,
                            checked=key == "toner",
                        )
                        for key in keys
                    ]
                    + [
                        dl.Overlay(dl.LayerGroup(markers), name="markers", checked=True),
                        dl.Overlay(dl.LayerGroup(polygon), name="polygon", checked=True),
                    ],
                    id="lc",
                )
            ],
            zoom=7,
            center=(56, 10),
            style={"height": "50vh"},
        ),
        html.Div(id="log"),
    ]
)


@app.callback(Output("log", "children"), Input("lc", "baseLayer"), Input("lc", "overlays"), prevent_initial_call=True)
def log(base_layer, overlays):
    return f"Base layer is {base_layer}, selected overlay(s): {json.dumps(overlays)}"


if __name__ == "__main__":
    app.run()
