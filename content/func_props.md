## Functional properties

In `dash-leaflet`, some component properties are *functions*. A function handle cannot be passed directly as a property in Dash, but the `dash-extensions` library provides a few implicit options. As an example, we consider the `GeoJSON` component of this package.

### JavaScript variables

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
    geojson = dl.GeoJSON(data=data, pointToLayer=ns("pointToLayer"))

For completeness, here is the full app,

.. dash-proxy:: content.func_props_js

### Inline JavaScript

The `assign` function of the `javascript` module provides a more compact syntax where the JavaScript code is written as a string directly in the Python file. The previous example is thus reduced to,

    import dash_leaflet as dl
    from dash_extensions.javascript import assign
    ...
    point_to_layer = assign("function(feature, latlng, context) {return L.circleMarker(latlng);}")
    geojson = dl.GeoJSON(data=data, pointToLayer=point_to_layer)

without the need for creating any `.js` files manually. The syntax is particularly well suited for small JavaScript code snippets and/or examples. Note that under the hood, the inline functions are transpiled into a `.js` file, which is written to the assets folder. For completeness, here is the full app,

.. dash-proxy:: content.func_props_inline

### Arrow functions

In some case, it might be sufficient to wrap an object as an arrow function, i.e. a function that just returns the (constant) object. The `dash-extensions` library supports this use case with the following syntax,

    from dash_extensions.javascript import arrow_function
    geojson = dl.GeoJSON(hoverStyle=arrow_function(dict(weight=5, color='#666', dashArray='')), ...)

For completeness, here is the full app,

.. dash-proxy:: content.func_props_arrow

