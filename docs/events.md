## Events

In Dash, interactivity is enabled by callbacks, which are triggered by *property changes*. In (native) Leaflet, interactivity is enabled by *events*. To make ends meet, we can add event handler(s) that trigger corresponding property change(s). However, as the Leaflet API is huge (the `Map` component, for example, exposes 36 separate events), adding handlers for all events would not only be tedious, but also hurt performance. Instead, `dash-leaflet` implements handlers for a number of default events (for ease of use), along with an interface to register custom event handlers (for maximum flexibility).

### Map click event

To get started, let's consider a map [click](https://leafletjs.com/reference.html#map-click) event. In Dash, it is custom to use an `n_clicks` property (similar to the `n_clicks` property of buttons) that is incremented on each click to signal change. In addition, we use a `clickData` property to forward relevant data associated with the event. Finally, to let Dash know about the property changes, we call the (special) `setProps` function, 

    ...
    click: function(e, ctx) {
        ctx.setProps({
            n_clicks: ctx.n_clicks == undefined ? 1 : ctx.n_clicks + 1,  // increment counter
            clickData: {
                latlng: e.latlng,
                layerPoint: e.layerPoint,
                containerPoint: e.containerPoint
            }  // collect data (must be JSON serializeable),
        });  // send data back to Dash
    }
    ...

With this event handler registered, we can now listen for click events from the map,

    ...
    app.callback(Output(...), Input('map', 'n_clicks'), State('clickData'))
    def onclick(_, data):
        print("You clicked at {data.latlng}")
    ...

### Default event handlers

Looking at the map click event example, you might notice a pattern. The event increments a counter property called `n_[event]s` and populates a data property called `[event]Data`. The same naming convention is followed by all the _default event handlers_,

* click
* dblclick
* keydown
* load (no data is set)

By default, the default event handlers are registered for all React Leaflet components that support them. Hence, you can have callbacks triggered on e.g. click or double click events via the `n_clicks` and `n_dblclicks` properties of a `Polygon` component (and many others). To disable the default event handlers, set the `disableDefaultEventHandlers` property to `True`.

### Custom event handlers

The `eventHandlers` property provides an interface to inject _custom_ event handlers. It is simply an object with the event name as key, and the event handler as value. The event handler is provided with three argument,

1) The event itself (e.g. for a click event, it would be a `LeafletMouseEvent` object)
2) A context object, which holds component props (including the `setProps` function) and a reference to the map container instance under the key `map`

As a simple example of event data usage, the following custom (click) event handler will extract the position you clicked on, and print it to the JS console,

.. dash-proxy:: docs.events_e

Via the 2nd argument, it is possible to manipulate the map object. The following custom event handler will fly to a specific location on right click,

.. dash-proxy:: docs.events_map

The 2nd argument can also be used to read/write component props. The following custom event handler will send data back to Dash on double click,

.. dash-proxy:: docs.events_set_props

