import json
import dash
import dash_html_components as html
import dash_leaflet as dl
from examples import us_states_js
from dash.dependencies import Output, Input
from dash_leaflet import express as dlx
from dash_extensions.transpile import module_to_props, inject_js

# Input data.
with open("assets/us-states.json", 'r') as f:
    data = json.load(f)


def get_info(feature=None):
    header = [html.H4("US Population Density")]
    if not feature:
        return header + ["Hoover over a state"]
    return header + [html.B(feature["properties"]["name"]), html.Br(),
                     "{:.3f} people / mi".format(feature["properties"]["density"]), html.Sup("2")]


# Create colorbar.
marks, color_scale = us_states_js.marks, us_states_js.color_scale
ctg = ["{}+".format(mark, marks[i + 1]) for i, mark in enumerate(marks[:-1])] + ["{}+".format(marks[-1])]
colorbar = dlx.categorical_colorbar(categories=ctg, colorscale=color_scale, width=300, height=30, position="bottomleft")
# Create geojson.
js = module_to_props(us_states_js)
geojson = dl.GeoJSON(data=data, hoverStyle=us_states_js.hover_style,
                     geojsonOptions=dict(style=us_states_js.style), id="geojson")
# Create info control.
info = html.Div(children=[html.H4("US Population Density")], id="info", className="info",
                style={"position": "absolute", "top": "10px", "right": "10px", "z-index": "1000"})
# Create app.
app = dash.Dash(prevent_initial_callbacks=True)
app.layout = html.Div([dl.Map(children=[dl.TileLayer(), geojson, colorbar, info], center=[39, -98], zoom=4)],
                      style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"}, id="map")
inject_js(app, js)


@app.callback(Output("info", "children"), [Input("geojson", "featureHover")])
def info_hover(feature):
    return get_info(feature)


if __name__ == '__main__':
    app.run_server()
