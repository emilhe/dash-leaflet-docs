import dash_leaflet as dl
from dash_extensions.enrich import DashProxy

image_bounds = [[40.712216, -74.22655], [40.773941, -74.12544]]
app = DashProxy()
app.layout = dl.Map([
    dl.ImageOverlay(opacity=0.5, url="/assets/newark_nj_1922.jpg", bounds=image_bounds), dl.TileLayer()
], bounds=image_bounds, style={'height': '50vh'})

if __name__ == '__main__':
    app.run()
