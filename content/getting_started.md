## Getting started

The easiest way to get started is to install the latest version of Dash and Dash Leaflet via pip,

```
pip install dash==1.15.0
pip install dash-leaflet==0.1.0
```

Additionally, if you plan on using the `GeoJSON` component, you'll also need geobuf and dash-transcrypt,

```
pip install dash-transcrypt==0.0.6
pip install geobuf==1.1.1
```

Once the installation is completed, paste the following lines of code into a .py file and run it.

````
import dash
import dash_leaflet as dl

app = dash.Dash()
app.layout = dl.Map(dl.TileLayer(), style={'width': '1000px', 'height': '500px'})

if __name__ == '__main__':
    app.run_server()    
````

That's it! You have now created your first interactive map with Dash Leaflet. If you visit http://127.0.0.1:8050/ in your browser, you should see a map similar to the one shown below. 