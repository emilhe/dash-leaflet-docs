## Getting started

The easiest way to get started is to install the latest version of Dash Leaflet via pip.

```
pip install dash-leaflet
```

Once the installation is completed, paste the following lines of code into a .py file a run it.

````
import dash
import dash_leaflet as dl

app = dash.Dash()
app.layout = dl.Map(dl.TileLayer(), style={'width': '1000px', 'height': '500px'})

if __name__ == '__main__':
    app.run_server()    
````

That's it! You have now created your first interactive map with Dash Leaflet. If you visit http://127.0.0.1:8050/ in your browser, you should see a map similar to the one shown below.

