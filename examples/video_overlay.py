import dash_leaflet as dl
from dash_extensions.enrich import DashProxy, html, Input, Output

video_urls = ["https://dash-leaflet.herokuapp.com/assets/patricia_nasa.mp4",
              "https://dash-leaflet.herokuapp.com/assets/patricia_nasa.webm"]
video_bounds = [[32, -130], [13, -100]]
app = DashProxy(prevent_initial_callbacks=True)
app.layout = html.Div([dl.Map([dl.TileLayer(),
                               dl.VideoOverlay(id="video", opacity=0.5, url=video_urls, bounds=video_bounds)],
                              bounds=[[32, -130], [13, -100]],
                              style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"}),
                       html.Button(id="play", children="Play/pause")])


@app.callback(Output("video", "play"), [Input("play", 'n_clicks')])
def play_pause(n):
    return n % 2 == 1


if __name__ == '__main__':
    app.run_server()
