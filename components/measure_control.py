import dash_leaflet as dl
from dash_extensions.enrich import DashProxy

app = DashProxy()
app.layout = dl.Map([
    dl.TileLayer(),
    dl.MeasureControl(position="topleft", primaryLengthUnit="kilometers", primaryAreaUnit="hectares",
                      activeColor="#214097", completedColor="#972158")
], center=[56, 10], zoom=6, style={'height': '50vh'})

if __name__ == '__main__':
    app.run_server()
