import importlib
import os
from collections import OrderedDict

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_leaflet as dl
from dash_extensions.snippets import fix_page_load_anchor_issue
from flask import Flask

# Example index.
example_labels = OrderedDict(
    tile_layer="TileLayer",
    map_click="Map click events",
    draw_polygon="Drawing polygons",
    layers_control="LayersControl",
    locate_control="Geolocation",
    # us_states="GeoJSON",
    polyline_decorator="PolylineDecorator",
    wsm_tile_layer="WMSTileLayer",
    image_overlay="ImageOverlay",
    video_overlay="VideoOverlay",
    geojson="GeoJSON",
    super_cluster="Marker clustering"
)
example_keys = list(example_labels.keys())
# Tutorial index.
tutorial_labels = OrderedDict(
    func_props="Function properties",
    choropleth_us="Choropleth map",
    scatter_us="Scatter plot"
)
tutorial_keys = list(tutorial_labels.keys())
# Container for app layouts.
app_layouts = {}


# region Util methods

def apply_prefix(prefix, component_id):
    if isinstance(component_id, dict):
        # TODO: How to implement this?
        # for key in component_id:
        #     if key == "index":
        #         continue
        #     component_id[key] = "{}-{}".format(prefix, component_id[key])
        return component_id
    return "{}-{}".format(prefix, component_id)


def prefix_id(arg, key):
    if hasattr(arg, 'component_id'):
        arg.component_id = apply_prefix(key, arg.component_id)
    if hasattr(arg, '__len__'):
        for entry in arg:
            entry.component_id = apply_prefix(key, entry.component_id)


def prefix_id_recursively(item, key):
    if hasattr(item, "id"):
        item.id = apply_prefix(key, item.id)
    if hasattr(item, "children"):
        children = item.children
        if hasattr(children, "id"):
            children.id = apply_prefix(key, children.id)
        if hasattr(children, "__len__"):
            for child in children:
                prefix_id_recursively(child, key)


def build_layout(app, wd, key):
    # Proxy that attaches callback to main app (with prefix).
    class AppProxy:

        def __init__(self, external_stylesheets=None, *args, **kwargs):
            self.layout = None
            self.external_stylesheets = external_stylesheets

        def callback(self, *args):
            for arg in list(args):
                prefix_id(arg, key)
            return app.callback(*args)

        @property
        def server(self):
            return app.server

        @property
        def index_string(self):
            return app.index_string

        @index_string.setter
        def index_string(self, value):
            app.index_string = value


    # Apply temporary monkey patch.
    dash_real = dash.Dash
    dash.Dash = AppProxy
    mod = importlib.import_module(f'{wd}.{key}')
    example = getattr(mod, "app")
    prefix_id_recursively(example.layout, key)
    app_layouts[key] = example.layout
    dash.Dash = dash_real

    return example.external_stylesheets


def render_example(key, label_map, wd):
    # Render markdown description.
    with open(f"{wd}/{key}.md", 'r') as f:
        info = dcc.Markdown(f.read())
    # Put everything together.
    elements = [
        html.A(id=key, className="anchor"), html.Br(),
        dbc.Row(dbc.Col(html.H4(label_map[key]))),
        dbc.Row(dbc.Col(info)),
    ]
    # Check if code is there.
    code_path = f"{wd}/{key}.py"
    if not os.path.isfile(code_path):
        return elements
    # Render app code.
    with open(code_path, 'r') as f:
        code = dcc.Markdown("````\n{}\n````".format(f.read()))
    # Put everything together.
    return elements + [html.Div([app_layouts[key], code], className="frame")]


def build_layouts(keys, wd):
    for key in keys:
        if not os.path.isfile(f"{wd}/{key}.py"):
            continue
        es = build_layout(app, wd, key)
        # Check that the example stylesheets are there.
        if not es:
            continue
        for item in es:
            if item not in app.config["external_stylesheets"]:
                raise ValueError("External stylesheet missing: {}".format(es))


# endregion

# region Elements

def landing_page():
    content = html.Div([
        dcc.Markdown("""Dash Leaflet is a wrapper of [Leaflet](https://leafletjs.com/), the leading open-source 
        JavaScript library for interactive maps. """),
        html.Img(src="assets/leaflet.png", style={"margin": "auto", "display": "block"}),
        dcc.Markdown("""The syntax is similar to other [Dash](https://plotly.com/dash/) components, with naming 
        conventions following [React-Leaflet](https://react-leaflet.js.org/). """)
    ])
    return [dbc.Row(dbc.Col(content, sm=12, md={"size": 8, "offset": 2}))]


def getting_started():
    with open("content/getting_started.md", 'r') as f:
        content = f.read()
    example = dl.Map(dl.TileLayer(), style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"})
    return [
        dbc.Row(dbc.Col([dcc.Markdown(content)])),
        dbc.Row(dbc.Col(example))  # , sm=12, md={"size": 10, "offset": 1})),
    ]


def components():
    with open("content/components.md", 'r') as f:
        content = f.read()
    return [dbc.Row(dbc.Col([dcc.Markdown(content)]))]


def examples():
    # Load intro.
    with open("content/examples.md", 'r') as f:
        content = f.read()
    # Load examples.
    example_bullets = []
    for key in example_keys:
        example_bullets.append("* [{}](/#{})".format(example_labels[key], key))
    return [dbc.Row(dbc.Col(dcc.Markdown(content))), dbc.Row(dbc.Col(dcc.Markdown("\n".join(example_bullets))))]


def tutorials():
    # Load intro.
    with open("content/tutorials.md", 'r') as f:
        content = f.read()
    # Load examples.
    tutorial_bullets = []
    for key in tutorial_keys:
        tutorial_bullets.append("* [{}](/#{})".format(tutorial_labels[key], key))
    return [dbc.Row(dbc.Col(dcc.Markdown(content))), dbc.Row(dbc.Col(dcc.Markdown("\n".join(tutorial_bullets))))]


# endregion

def get_content():
    content = [html.A(id="home", className="anchor"), html.Br()] + landing_page() + \
              [html.A(id="start", className="anchor"), html.Hr()] + getting_started() + \
              [html.A(id="components", className="anchor"), html.Hr()] + components() + \
              [html.A(id="examples", className="anchor"), html.Hr()] + examples()
    # Add examples.
    for key in example_keys:
        content += render_example(key, example_labels, "examples")
    content += [html.A(id="tutorials", className="anchor"), html.Hr()] + tutorials()
    # Add tutorials.
    for key in tutorial_keys:
        content += render_example(key, tutorial_labels, "tutorials")
    return content


def get_nav():
    examples_links = [dbc.NavItem(dbc.NavLink(example_labels[key],
                                              href="/#{}".format(key), external_link=True)) for key in example_keys]
    tutorial_links = [dbc.NavItem(dbc.NavLink(tutorial_labels[key],
                                              href="/#{}".format(key), external_link=True)) for key in tutorial_keys]
    return dbc.NavbarSimple(
        dbc.Nav([
            # Other links.
            dbc.NavItem(dbc.NavLink("Home", href="/#", external_link=True)),
            dbc.NavItem(dbc.NavLink("Getting started", href="/#start", external_link=True)),
            dbc.NavItem(dbc.NavLink("Components", href="/#components", external_link=True)),
            # Example links.
            dbc.NavItem(dbc.NavLink("Examples", href="/#examples", external_link=True,
                                    style={"margin-left": "100px"})),
            dbc.DropdownMenu(
                label="", children=examples_links, in_navbar=True, nav=True, direction="left",
                style={"margin-left": "0px"}),
            # Tutorials links.
            dbc.NavItem(dbc.NavLink("Tutorials", href="/#tutorials", external_link=True)),
            dbc.DropdownMenu(
                label="", children=tutorial_links, in_navbar=True, nav=True, direction="left",
                style={"margin-right": "0px"})
            ,
        ],
            fill=True), fluid=True, sticky="top")


ext_js = ["https://cdnjs.cloudflare.com/ajax/libs/chroma-js/2.1.0/chroma.min.js"]
ext_css = [dbc.themes.CERULEAN, 'https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css']
# Create app.
server = Flask(__name__)
app = dash.Dash(server=server, external_stylesheets=ext_css, external_scripts=ext_js, prevent_initial_callbacks=True)
# Register examples.
build_layouts(example_keys, "examples")
build_layouts(tutorial_keys, "tutorials")
# Setup layout.
app.layout = html.Div([get_nav(), dbc.Container(get_content(), id="content")] +
                      fix_page_load_anchor_issue(app, delay=650))

if __name__ == '__main__':
    app.run_server(port=7779)
