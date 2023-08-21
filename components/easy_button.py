import dash_leaflet as dl
from dash_extensions.enrich import DashProxy, html, Output, Input

# Add CSS that for the icon.
external_css = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"
# Create example app.
app = DashProxy(external_stylesheets=[external_css])
app.layout = html.Div([
    dl.Map([
        dl.TileLayer(),
        dl.EasyButton(icon="fa-globe", title="So easy", id="btn")
    ], center=[56, 10], zoom=6, style={'height': '50vh'}),
    html.Div(id="log")
])


@app.callback(Output("log", "children"), Input("btn", "n_clicks"))
def log(n_clicks):
    return f"You clicked the button {n_clicks} times."


if __name__ == "__main__":
    app.run_server()
