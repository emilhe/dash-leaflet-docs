import {discrete} from './choropleth.js'

window.dash_props = Object.assign({}, window.dash_props, {
    choropleth: {
        discrete
    }
});
