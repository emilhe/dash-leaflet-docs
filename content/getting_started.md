## Getting started

The easiest way to get started is to install the latest version of `dash`, `dash-leaflet` and (optionally) `dash-extensions` via pip,

```
pip install dash==2.0.0
pip install dash-leaflet==0.1.18
pip install dash-extensions==0.0.62
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