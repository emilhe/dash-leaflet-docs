import uuid
import dash_leaflet as dl
from dash_extensions.enrich import DashProxy, html, Output, Input


app = DashProxy(prevent_initial_callbacks=True)
app.layout = html.Div([
    html.Div(
        dl.Map(dl.TileLayer(), center=[56, 10], zoom=6, id="my_map", style=dict(height='50vh')),
        id="map_container"
    ),
    html.Button("Change zoom (same id)", id="btn"),
    html.Button("Change zoom (different id)", id="btn_unique")
])


@app.callback(Output("map_container", "children", allow_duplicate=True),
              Input("btn", "n_clicks"))
def log(_):
    # Same id, triggers update, will NOT work since zoom is immutable
    same_id = "getting_started-my_map"
    return dl.Map(dl.TileLayer(), center=[56, 10], zoom=12, style=dict(height='50vh'), id=same_id)


@app.callback(Output("map_container", "children"),
              Input("btn_unique", "n_clicks"))
def log(_):
    # Different id, triggers re-creation, thus works
    different_id = str(uuid.uuid4())
    return dl.Map(dl.TileLayer(), center=[56, 10], zoom=12, style=dict(height='50vh'), id=different_id)


if __name__ == '__main__':
    app.run_server(debug=True)
