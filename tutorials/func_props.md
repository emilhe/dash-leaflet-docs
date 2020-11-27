In Dash Leaflet, some component properties are *functions*. A function handle cannot be passed directly as a property in Dash, but the `dash-extensions` library provides a few implicit options. As an example, we consider the `pointToLayer` option of the `GeoJSON` component.

##### JavaScript variables

The `dash-extensions` library enables mapping of variables in the (global) `window` object into component properties.  Hence, if we create a `.js` file in the assets folder with the following content,

	window.myNamespace = Object.assign({}, window.myNamespace, {  
	    mySubNamespace: {  
	        pointToLayer: function(feature, latlng, context) {  
	            return L.circleMarker(latlng)  
	        }  
	    }  
	});

the `pointToLayer` function of the `myNamespace.mySubNamespace` namespace can be used as a component property,

    import dash_leaflet as dl
    from dash_extensions.javascript import Namespace
    
    ns = Namespace("myNamespace", "mySubNamespace")
    geojson = dl.GeoJSON(data=data, options=dict(pointToLayer=ns("pointToLayer")))

For completeness, here is the full app,

	import random  
	import dash  
	import dash_html_components as html  
	import dash_leaflet as dl  
	import dash_leaflet.express as dlx  
    from dash_extensions.javascript import Namespace

	# Create some markers.  
	points = [dict(lat=55.5 + random.random(), lon=9.5 + random.random(), value=random.random()) for i in range(100)]  
	data = dlx.dicts_to_geojson(points)  
	# Create geojson.  
    ns = Namespace("myNamespace", "mySubNamespace")
    geojson = dl.GeoJSON(data=data, options=dict(pointToLayer=ns("pointToLayer")))
	# Create the app.  
	app = dash.Dash()  
	app.layout = html.Div([  
	    dl.Map([dl.TileLayer(), geojson], center=(56, 10), zoom=8, style={'height': '50vh'}),  
	])  
	  
	if __name__ == '__main__':  
	    app.run_server()

##### Dash leaflet express

For some function properties, a [selection of functions](https://github.com/thedirtyfew/dash-leaflet/blob/master/src/lib/express.js) that address some of the most common use cases are included in the `dlx` namespace. For the `GeoJSON` component, these functions reside in the `scatter` and `choropleth` subnamespaces. As an example, here is a full app code for a scatter plot,

    import random
    import dash
    import dash_html_components as html
    import dash_leaflet as dl
    import dash_leaflet.express as dlx
    from dash_extensions.javascript import Namespace
    
    # Create some markers.
    points = [dict(lat=55.5 + random.random(), lon=9.5 + random.random(), value=random.random()) for i in range(100)]
    data = dlx.dicts_to_geojson(points)
    # Create geojson.
    ns = Namespace("dlx", "scatter")
    geojson = dl.GeoJSON(data=data, options=dict(pointToLayer=ns("pointToLayer")))
    # Create the app.
    app = dash.Dash(external_scripts=["https://cdnjs.cloudflare.com/ajax/libs/chroma-js/2.1.0/chroma.min.js"])
    app.layout = html.Div([
        dl.Map([dl.TileLayer(), geojson], center=(56, 10), zoom=8, style={'height': '50vh'}),
    ])
    
    if __name__ == '__main__':
        app.run_server()

Note the import of the `chroma-js` library. Any external JavaScript library used by the rendering functions should be added as `external_scripts`, in this case the  `chroma-js` library.