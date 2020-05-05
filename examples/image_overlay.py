import dash
import dash_html_components as html
import dash_leaflet as dl

image_url = "https://raw.githubusercontent.com/thedirtyfew/dash-leaflet/master/assets/newark_nj_1922.jpg"
image_bounds = [[40.712216, -74.22655], [40.773941, -74.12544]]
app = dash.Dash()
app.layout = html.Div([dl.Map([dl.ImageOverlay(opacity=0.5, url=image_url, bounds=image_bounds), dl.TileLayer()],
                              bounds=image_bounds,
                              style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"})])

if __name__ == '__main__':
    app.run_server()
