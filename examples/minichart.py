from dash_extensions.enrich import Dash, Output, Input, dcc
import dash_leaflet as dl

# Create example app.
app = Dash()
app.layout = dl.Map([
    dl.TileLayer(),
    dl.Minichart(lat=56.1780842, lon=10.1119354, type="bar", id="bar"),
    dl.Minichart(lat=55.6712474, lon=12.5237848, type="pie", id="pie"),
    dcc.Interval(id="trigger")
], style={'width': '1000px', 'height': '500px'})
# Do animated updates (could also be normal callback, but clientside is more performant).
app.clientside_callback("""
function(n_intervals){
    const fakeData = () => [Math.random(), Math.random(), Math.random(), Math.random(), Math.random()]
    return [fakeData(), fakeData()]
}
""", [Output("bar", "data")], [Output("pie", "data")], Input("trigger", "n_intervals"))

if __name__ == '__main__':
    app.run_server()
