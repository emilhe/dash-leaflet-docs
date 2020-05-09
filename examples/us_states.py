import dash
import dash_html_components as html
import json
import dash_leaflet as dl
from dash.dependencies import Output, Input
from dash_leaflet import express as dlx

# Input data.
with open("assets/us-states.json", 'r') as f:
    data = json.load(f)
marks = [0, 10, 20, 50, 100, 200, 500, 1000]
colorscale = ['#FFEDA0', '#FED976', '#FEB24C', '#FD8D3C', '#FC4E2A', '#E31A1C', '#BD0026', '#800026']


def get_style(feature):
    color = [colorscale[i] for i, item in enumerate(marks) if feature["properties"]["density"] > item][-1]
    return dict(fillColor=color, weight=2, opacity=1, color='white', dashArray='3', fillOpacity=0.7)


def get_info(feature=None):
    header = [html.H4("US Population Density")]
    if not feature:
        return header + ["Hoover over a state"]
    return header + [html.B(feature["properties"]["name"]), html.Br(),
                     "{:.3f} people / mi".format(feature["properties"]["density"]), html.Sup("2")]


# Create colorbar.
ctg = ["{}+".format(mark, marks[i + 1]) for i, mark in enumerate(marks[:-1])] + ["{}+".format(marks[-1])]
colorbar = dlx.categorical_colorbar(categories=ctg, colorscale=colorscale, width=300, height=30, position="bottomleft")
# Create geojson.
options = dict(hoverStyle=dict(weight=5, color='#666', dashArray=''), zoomToBoundsOnClick=True)
geojson = dlx.geojson(data, id="geojson", options=options, style=get_style)
# Create info control.
info = html.Div(children=get_info(), id="info", className="info",
                style={"position": "absolute", "top": "10px", "right": "10px", "z-index": "1000"})
# Create app.
app = dash.Dash(prevent_initial_callbacks=True,
                external_stylesheets=["https://dash-leaflet.herokuapp.com/assets/geojson.css"])
app.layout = html.Div([dl.Map(children=[dl.TileLayer(), geojson, colorbar, info], center=[39, -98], zoom=4)],
                      style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"})


@app.callback(Output("info", "children"), [Input("geojson", "featureHover")])
def info_hover(feature):
    return get_info(feature)


if __name__ == '__main__':
    app.run_server()
