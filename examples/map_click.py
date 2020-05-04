import json
import dash
import dash_html_components as html
import dash_leaflet as dl

from dash.dependencies import Input, Output

app = dash.Dash()
app.layout = html.Div([
    dl.Map(dl.TileLayer(), id="map", style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"}),
    html.Div(id="click_text")
])

@app.callback(Output("click_text", "children"), [Input("map", "click_lat_lng")])
def map_click(e):
    if e is None:
        return "No click yet"
    return "You clicked @ {}".format(json.dumps(e))

if __name__ == '__main__':
    app.run_server()
