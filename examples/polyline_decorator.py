import dash_leaflet as dl
from dash_extensions.enrich import DashProxy, html

# Simple arrow.
polyline = dl.Polyline(positions=[[57, -19], [60, -12]])
patterns = [dict(offset='100%', repeat='0', arrowHead=dict(pixelSize=15, polygon=False, pathOptions=dict(stroke=True)))]
arrow = dl.PolylineDecorator(children=polyline, patterns=patterns)
# Polygon with inner ring.
polygon = dl.Polygon(color="#ff7800", weight=1, positions=[[[54, -6], [55, -7], [56, -2], [55, 1], [53, 0]],
                                                           [[54, -3], [54, -2], [55, -1], [55, -5]]])
patterns = [dict(offset='0', repeat='10', dash=dict(pixelSize=0))]
inner_ring = dl.PolylineDecorator(children=polygon, patterns=patterns)
# Multi-pattern without polyline.
patterns = [dict(offset='12', repeat='25', dash=dict(pixelSize=10, pathOptions=dict(color='#f00', weight=2))),
            dict(offset='0', repeat='25', dash=dict(pixelSize=0))]
positions = [[49.543519, -12.469833], [49.808981, -12.895285], [50.056511, -13.555761], [50.217431, -14.758789],
             [44.833574, -25.346101], [44.039720, -24.988345]]
multi_pattern = dl.PolylineDecorator(positions=positions, patterns=patterns)
# Markers proportionally located.
patterns = [dict(offset='5%', repeat='10%', marker={})]
polyline = dl.Polyline(positions=[[58.44773, -28.65234], [52.9354, -23.33496], [53.01478, -14.32617],
                                  [58.1707, -10.37109], [59.68993, -0.65918]])
marker_pattern = dl.PolylineDecorator(children=polyline, patterns=patterns)
# Rotated custom marker.
iconUrl = "https://dash-leaflet.herokuapp.com/assets/icon_plane.png"
marker = dict(rotate=True, markerOptions=dict(icon=dict(iconUrl=iconUrl, iconAnchor=[16, 16])))
patterns = [dict(repeat='10', dash=dict(pixelSize=5, pathOptions=dict(color='#000', weight=1, opacity=0.2))),
            dict(offset='16%', repeat='33%', marker=marker)]
rotated_markers = dl.PolylineDecorator(positions=[[42.9, -15], [44.18, -11.4], [45.77, -8.0], [47.61, -6.4],
                                                  [49.41, -6.1], [51.01, -7.2]], patterns=patterns)
# Create app.
app = DashProxy()
app.layout = html.Div(dl.Map([dl.TileLayer(), arrow, inner_ring, multi_pattern, marker_pattern, rotated_markers],
                             zoom=4, center=(52.0, -11.0)),
                      style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"})

if __name__ == '__main__':
    app.run_server()
