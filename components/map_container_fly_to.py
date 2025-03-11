import dash_leaflet as dl
from dash_extensions.enrich import DashProxy, html, Output, Input

app = DashProxy()
app.layout = html.Div([
    dl.Map([
        dl.TileLayer()
    ], center=[56, 10], zoom=6, style={'height': '50vh'}, id="map"),
    html.Button("Fly to Paris", id="btn")
])


@app.callback(Output("map", "viewport"), Input("btn", "n_clicks"), prevent_initial_call=True)
def fly_to_paris(_):
    return dict(center=[48.864716, 2.349014], zoom=10, transition="flyTo")


if __name__ == '__main__':
    app.run()
