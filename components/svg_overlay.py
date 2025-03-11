import dash_leaflet as dl
from dash_extensions.enrich import DashProxy
from dash_svg import Rect

bounds = [[56, 10], [55, 9]]
app = DashProxy()
app.layout = dl.Map([
    dl.TileLayer(),
    dl.SVGOverlay(
        children=[
            Rect(width=200, height=200),
        ],
        attributes=dict(
            stroke='red',
            viewbox="0 0 200 200",
            xmlns="http://www.w3.org/2000/svg"
        ), bounds=bounds,
    )
], center=[56, 10], zoom=8, style={'height': '50vh'})

if __name__ == '__main__':
    app.run(debug=True)
