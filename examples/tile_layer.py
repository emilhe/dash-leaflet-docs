import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_leaflet as dl

from dash.dependencies import Output, Input

# Create options.
keys = ["watercolor", "toner", "terrain"]
url_template = "http://{{s}}.tile.stamen.com/{}/{{z}}/{{x}}/{{y}}.png"
options = [{"label": key, "value": url_template.format(key)} for key in keys]
default_url = options[0]["value"]
dd_style = {"position": "relative", "bottom": "50px", "left": "10px", "z-index": "1000", "width": "200px"}
# Create app.
app = dash.Dash(prevent_initial_callbacks=True)
app.layout = html.Div([
    dl.Map([dl.TileLayer(id="tiles", url=default_url)]),
    html.Div(dcc.Dropdown(options=options, id="dropdown", value=default_url), style=dd_style)
], style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block", "position": "relative"})


@app.callback(Output("tiles", "url"), [Input("dropdown", "value")])
def update_provider(provider):
    return provider


if __name__ == '__main__':
    app.run_server()
