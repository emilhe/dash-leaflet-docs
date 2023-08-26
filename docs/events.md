## Events

In Dash, interactivity is enabled by *callbacks*, which are triggered by *property changes*. In (native) Leaflet, interactivity is enabled by *events*. To make ends meet, event handler(s) that trigger corresponding property change(s) are needed. However, as the Leaflet API is huge (the `Map` component, for example, exposes 36 separate events), adding handlers for all events would not only be tedious, but also hurt performance. Instead, `dash-leaflet` implements handlers for a limited number of events (for ease of use), and exposes an interface to register custom event handlers (for maximum flexibility).

### Map click event

To illustrate the concept, let's consider a map [click](https://leafletjs.com/reference.html#map-click) event. In Dash, it is custom to increment an `n_clicks` property (e.g. the `n_clicks` property of buttons) on each click (to signal _change_). Additionally, relevant data are typically exposed though a `clickData` property (e.g. the `clickData` property of the `Graph` component). Following these conventions, we implement the following click event handler,

    ...
    click: function(e: LeafletMouseEvent, ctx) {
        ctx.setProps({
            n_clicks: ctx.n_clicks == undefined ? 1 : ctx.n_clicks + 1,  // increment counter
            clickData: {
                latlng: e.latlng,
                layerPoint: e.layerPoint,
                containerPoint: e.containerPoint
            }  // collect data (must be JSON serializeable)
        });  // send data back to Dash
    }
    ...

Note the special [`setProps` function](https://dash.plotly.com/react-for-python-developers), which relays data back to Dash. With this event handler registered, we can now listen for click events from the map,

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

All of the default event handlers are registered on the `Map` component. For other components, only relevant events handlers are registered. To disable the default event handlers, set the `disableDefaultEventHandlers=True`.

### Custom event handlers

The `eventHandlers` property provides an interface to inject _custom_ event handlers. It is simply an object with the event name as key, and the event handler as value. The event handler is passed the original event data (e.g. for a click event, it would be a `LeafletMouseEvent` object), along with a context object, which holds component props (including the `setProps` function) and a reference to the map container instance (under the key `map`).

As a simple example of event data usage, the following custom (click) event handler will extract the position you clicked on, and print it to the JS console,

.. dash-proxy:: docs.events_e

Via the context argument, it is possible to manipulate the map object. The following custom event handler will fly to a specific location on right click,

.. dash-proxy:: docs.events_map

The context argument can also be used to read/write component props. The following custom event handler will send data back to Dash on double click,

.. dash-proxy:: docs.events_set_props

### Control event handlers

Note that many controls (e.g. `FullScreenControl`, `LocateControl`, `MeasureControl`, `LayerControl`) expose events through the map component, not the control itself. Hence, to register an event handler when a measurement performed via the `MeasureControl` is finished, you would register the appropriate event handler on the map itself,

.. dash-proxy:: docs.measure_control_event
   :prefix: measure_control_event
