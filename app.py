import importlib
from collections import OrderedDict

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_leaflet as dl
from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate
from flask import Flask

print(dash.__version__)

# Example index.
example_labels = OrderedDict(
    map_click="Map click events",
    draw_polygon="Drawing polygons",
    locate_control="Geolocation",
    marker_cluster="Marker cluster",
    wsm_tile_layer="WMSTileLayer",
    image_overlay="ImageOverlay",
    video_overlay="VideoOverlay"
)
example_keys = list(example_labels.keys())
example_layouts = {}


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


def register_example(app, key):
    # Proxy that attaches callback to main app (with prefix).
    class AppProxy:

        def __init__(self, external_stylesheets=None, *args, **kwargs):
            self.layout = None
            self.external_stylesheets = external_stylesheets

        def callback(self, *args):
            for arg in list(args):
                prefix_id(arg, key)
            return app.callback(*args)

    # Apply temporary monkey patch.
    dash_real = dash.Dash
    dash.Dash = AppProxy
    mod = importlib.import_module('examples.{}'.format(key))
    example = getattr(mod, "app")
    prefix_id_recursively(example.layout, key)
    example_layouts[key] = example.layout
    dash.Dash = dash_real

    return example.external_stylesheets


def render_example(key):
    # Render markdown description.
    with open("examples/{}.md".format(key), 'r') as f:
        info = dcc.Markdown(f.read())
    # Render app code.
    with open("examples/{}.py".format(key), 'r') as f:
        code = dcc.Markdown("````\n{}\n````".format(f.read()))
    # Put everything together.
    return [html.A(id=key, className="anchor"), html.Br()] + \
           [
               dbc.Row(dbc.Col(html.H4(example_labels[key]))),
               dbc.Row(dbc.Col(info)),
               html.Div([example_layouts[key], code], className="frame")
               # )
               # dbc.Container([
               #     dbc.Row(dbc.Col(example_layouts[key])), #, sm=12, md={"size": 10, "offset": 1})),
               #     dbc.Row(dbc.Col(html.Br())),
               #     dbc.Row(dbc.Col(code))
               # ],  className="frame")
           ]


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
    # TODO: What about this block?

    # Load intro.
    with open("content/examples.md", 'r') as f:
        content = f.read()
    # Load examples.
    example_bullets = []
    for key in example_keys:
        example_bullets.append("* [{}](/#{})".format(example_labels[key], key))
    return [dbc.Row(dbc.Col(dcc.Markdown(content))), dbc.Row(dbc.Col(dcc.Markdown("\n".join(example_bullets))))]


# endregion

def get_content():
    return [html.A(id="home", className="anchor"), html.Br()] + landing_page() + \
           [html.A(id="start", className="anchor"), html.Hr()] + getting_started() + \
           [html.A(id="components", className="anchor"), html.Hr()] + components() + \
           [html.A(id="examples", className="anchor"), html.Hr()] + examples()


def get_nav():
    examples_links = [dbc.NavItem(dbc.NavLink(example_labels[key],
                                              href="/#{}".format(key), external_link=True)) for key in example_keys]
    return dbc.NavbarSimple(
        dbc.Nav([dbc.NavItem(dbc.NavLink("Home", href="/#", external_link=True)),
                 dbc.NavItem(dbc.NavLink("Getting started", href="/#start", external_link=True)),
                 dbc.NavItem(dbc.NavLink("Components", href="/#components", external_link=True)),
                 # Example links.
                 dbc.NavItem(dbc.NavLink("Examples", href="/#examples", external_link=True,
                                         style={"margin-left": "100px"})),
                 dbc.DropdownMenu(
                     label="", children=examples_links, in_navbar=True, nav=True, direction="left",
                     style={"margin-left": "0px"})
                 ],
                fill=True), fluid=True, sticky="top")


ext_css = [dbc.themes.CERULEAN, 'https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css']
# Create app.
server = Flask(__name__)
app = dash.Dash(server=server, external_stylesheets=ext_css, prevent_initial_callbacks=True)
# Register examples.
for key in example_keys:
    es = register_example(app, key)
    # Check that the example stylesheets are there.
    if not es:
        continue
    for item in es:
        if item not in app.config["external_stylesheets"]:
            raise ValueError("External stylesheet missing: {}".format(es))
# Setup layout.
app.layout = html.Div([get_nav(), dbc.Container(id="content"), dcc.Location(id="url")])


# Index callbacks
@app.callback(Output('content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    # Main pages.
    if pathname == "/":
        base_page = get_content()
        for key in example_keys:
            base_page += render_example(key)
        return base_page
    # Example pages.
    key = pathname.split("/")[1]
    if key in example_keys:
        return render_example(key)
    return "Page not found ({})".format(pathname)


if __name__ == '__main__':
    app.run_server(debug=False, port=8051)
