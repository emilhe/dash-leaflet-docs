This example demonstrates how the `GeoJSON` component can be utilized to create an interactive choropleth map of the US population density. It is essentially a reproduction of the [interactive choropleth map](https://leafletjs.com/examples/choropleth/) in the Leaflet example gallery, but with a few tweaks. 

Rather than creating a legend control from scratch to visualize the (categorical) color scale, the Dash Leaflet `Colorbar` component is used. 

To illustrate how interactivity can be achieved via Dash, the info control (which shows feature details on hover) is now created in Python. The info is updated via a Dash callback that takes the `featureHover` property as a input. Similarly, the `GeoJSON` component also has `featureClick` property (though it is not used in the example). 

Interactivity via Dash requires communication with the server, which means that a JavaScript implementation will typically be more responsive. Therefore, common interactivity patterns, such as zoom-on-click, change-style-on-hover and show-popup-on-click, have been implemented as part of the `GeoJSON` component. Hence, while it was necessary in the original Leaflet example to write explicit code to achieve these behaviors, in Dash Leaflet they can be achieved by setting the appropriate flags of the `options` property in the `GeoJSON` component.

NB: To run the example, you need to put [us-states.json](https://dash-leaflet.herokuapp.com/assets/us-states.json) in your assets folder.