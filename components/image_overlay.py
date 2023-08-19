import dash_leaflet as dl
from dash_extensions.enrich import DashProxy, html

image_url = "https://dash-leaflet.herokuapp.com/assets/newark_nj_1922.jpg"
image_bounds = [[40.712216, -74.22655], [40.773941, -74.12544]]
app = DashProxy()
app.layout = dl.Map([
    dl.ImageOverlay(opacity=0.5, url=image_url, bounds=image_bounds), dl.TileLayer()
], bounds=image_bounds, style={'width': '100%', 'height': '50vh'})

if __name__ == '__main__':
    app.run_server()
