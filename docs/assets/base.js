window.myNamespace = Object.assign({}, window.myNamespace, {
    mySubNamespace: {
        pointToLayer: function(feature, latlng, context) {
            return L.circleMarker(latlng)
        }
    }
});