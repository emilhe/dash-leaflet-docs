In Dash leaflet, some component properties are *functions*. Since a function handle cannot be passed as a property in Dash, instead the *full path to the function* must be provided as a string. As an example, we consider the `pointToLayer` option of the `GeoJSON` component.

##### JavaScript functions

The most direct way to make function(s) available is to create a `.js` file in the assets folder,

	window.dash_props = Object.assign({}, window.dash_props, {  
	    module: {  
	        point_to_layer: function(feature, latlng, context) {  
	            return L.circleMarker(latlng)  
	        }  
	    }  
	});

The full path to this function is `window.dash_props.module.point_to_layer`, i.e. the GeoJSON object would be initialized like this,

	geojson = dl.GeoJSON(..., options = dict(pointToLayer = "window.dash_props.module.point_to_layer"))

For completeness, here is the full app,

	import random  
	import dash  
	import dash_html_components as html  
	import dash_leaflet as dl  
	import dash_leaflet.express as dlx  
	  
	# Create some markers.  
	points = [dict(lat=55.5 + random.random(), lon=9.5 + random.random(), value=random.random()) for i in range(100)]  
	data = dlx.dicts_to_geojson(points)  
	# Create geojson.  
	geojson = dl.GeoJSON(data=data, options=dict(pointToLayer="window.dash_props.module.point_to_layer"))  
	# Create the app.  
	app = dash.Dash()  
	app.layout = html.Div([  
	    dl.Map([dl.TileLayer(), geojson], center=(56, 10), zoom=8, style={'height': '50vh'}),  
	])  
	  
	if __name__ == '__main__':  
	    app.run_server()

##### Python functions

The function can also be written in Python, this is made possible via [`dash-transcrypt`](https://pypi.org/project/dash-transcrypt/). Create a separate  `.py` file say that contains the function(s),

    def point_to_layer(feature, latlng, context):  
        return L.circleMarker(latlng)

Passing the module through the `module_to_props` functions, the Python code is transpiled to JavaScript and the function attributes are replaced by the full path to the function.  Hence, the GeoJSON object can now be initialized like this,

	js = module_to_props(module)  
	geojson = dl.GeoJSON(..., options=dict(pointToLayer=module.point_to_layer))
	...
	inject_js(app, js)

The `module_to_props` function returns the path to a generated javascript index file, which can be registered on the app via the `inject_js` function. For completeness, here is the full app,

	import random  
	import dash  
	import dash_html_components as html  
	import dash_leaflet as dl  
	import prop_funcs as pf  # module containing the point_to_layer function  
	import dash_leaflet.express as dlx  
	  
	from dash_transcrypt import inject_js, module_to_props  
	  
	# Create some markers.  
	points = [dict(lat=55.5 + random.random(), lon=9.5 + random.random(), value=random.random()) for i in range(100)]  
	data = dlx.dicts_to_geojson(points)  
	# Create geojson.  
	js = module_to_props(pf)  
	geojson = dl.GeoJSON(data=data, options=dict(pointToLayer=pf.point_to_layer))  
	# Create the app.  
	app = dash.Dash()  
	app.layout = html.Div([  
	    dl.Map([dl.TileLayer(), geojson], center=(56, 10), zoom=8, style={'height': '50vh'}),  
	])  
	inject_js(app, js)  
	  
	if __name__ == '__main__':  
	    app.run_server()

##### Dash leaflet functions

For some function properties, Dash Leaflet contains a selection of functions that address some of the most common use cases. If one of these functions fit your needs, simply import the function and use it like any other function. For the `GeoJSON` component, these functions reside in the `geojson` module.  As an example, here is a full app code for a scatter plot,

	import random  
	import dash  
	import dash_html_components as html  
	import dash_leaflet as dl  
	import dash_leaflet.express as dlx  
	  
	from dash_leaflet.geojson import scatter  
	from dash_transcrypt import inject_js, module_to_props  
	  
	# Create some markers.  
	points = [dict(lat=55.5 + random.random(), lon=9.5 + random.random(), value=random.random()) for i in range(100)]  
	data = dlx.dicts_to_geojson(points)  
	# Create geojson.  
	js = module_to_props(scatter)  
	geojson = dl.GeoJSON(data=data, options=dict(pointToLayer=scatter.point_to_layer))  
	# Create the app.  
	app = dash.Dash(external_scripts=["https://cdnjs.cloudflare.com/ajax/libs/chroma-js/2.1.0/chroma.min.js"])  # neede by t
	app.layout = html.Div([  
	    dl.Map([dl.TileLayer(), geojson], center=(56, 10), zoom=8, style={'height': '50vh'}),  
	])  
	inject_js(app, js)  
	 
	if __name__ == '__main__':  
	    app.run_server()

Note the import of the `chroma-js` library. Any JavaScript library used by the transpiled functions should be added as `external_scripts`, in this case the  `chroma-js` library.

##### Passing additional arguments

It is possible to pass arguments to the Python functions both at compile time and runtime, see the [dash-transcrypt documentation](https://github.com/thedirtyfew/dash-transcrypt/#passing-arguments-at-compile-time) for details.