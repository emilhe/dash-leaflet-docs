import dash_leaflet as dl
from dash_extensions.enrich import DashProxy, Input, Output, html

video_bounds = [[32, -130], [13, -100]]
app = DashProxy()
app.layout = html.Div(
    [
        dl.Map(
            [
                dl.TileLayer(),
                dl.VideoOverlay(
                    id="video",
                    opacity=0.5,
                    bounds=video_bounds,
                    play=True,
                    url=["/assets/patricia_nasa.mp4", "/assets/patricia_nasa.webm"],
                ),
            ],
            bounds=[[32, -130], [13, -100]],
            style={"height": "50vh"},
        ),
        html.Button(id="play", children="Play/pause"),
    ]
)


@app.callback(Output("video", "play"), [Input("play", "n_clicks")], prevent_initial_call=True)
def play_pause(n):
    return n % 2 == 0


if __name__ == "__main__":
    app.run()
