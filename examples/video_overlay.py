import dash
import dash_html_components as html
import dash_leaflet as dl
from dash.dependencies import Input, Output

video_url = "https://dash-leaflet.herokuapp.com/assets/patricia_nasa.webm"
video_bounds = [[32, -130], [13, -100]]
app = dash.Dash()
app.layout = html.Div([dl.Map([dl.TileLayer(),
                               dl.VideoOverlay(id="video", opacity=0.5, url=video_url, bounds=video_bounds)],
                              bounds=[[32, -130], [13, -100]],
                              style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"}),
                       html.Button(id="play", children="Play/pause")])


@app.callback(Output("video", "play"), [Input("play", 'n_clicks')])
def play_pause(n):
    return n is not None and n % 2 == 1


if __name__ == '__main__':
    app.run_server()
