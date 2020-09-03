import {_get_color,_resolve_options,bind_popup,cluster_to_layer,point_to_layer} from './scatter.js'

window.dash_props = Object.assign({}, window.dash_props, {
    scatter: {
        _get_color,_resolve_options,bind_popup,cluster_to_layer,point_to_layer
    }
});
