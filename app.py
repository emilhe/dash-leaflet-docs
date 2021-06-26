import os
import importlib
import dash_leaflet as dl
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from dash_extensions.enrich import Dash
from dash_extensions.snippets import fix_page_load_anchor_issue
from dash_extensions.multipage import app_to_page
from collections import OrderedDict
from flask import Flask

# Example index.
example_labels = OrderedDict(
    tile_layer="TileLayer",
    map_click="Map click events",
    # draw_polygon="Drawing polygons",
    layers_control="LayersControl",
    geojson="GeoJSON",
    super_cluster="Marker clustering",
    locate_control="Geolocation",
    measure="MeasureControl",
    # us_states="GeoJSON",
    polyline_decorator="PolylineDecorator",
    wsm_tile_layer="WMSTileLayer",
    image_overlay="ImageOverlay",
    video_overlay="VideoOverlay",
)
example_keys = list(example_labels.keys())
# Tutorial index.
tutorial_labels = OrderedDict(
    geojson_filter="Feature filtering",
    geojson_hideout="Interactivity via the hideout prop",
    scatter_plot="Scatter plot",
    geojson_icon="Custom icons",
    scatter_cluster="Custom cluster icons",
    choropleth_us="Choropleth map",
)
tutorial_keys = list(tutorial_labels.keys())


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


def func_props():
    with open("content/func_props.md", 'r') as f:
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
    return [dbc.Row(dbc.Col(dcc.Markdown(content))),
            dbc.Row(dbc.Col(dcc.Markdown("\n".join(example_bullets))))]


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

def build_example(app, key, label_map, wd):
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
    # Create the app page.
    mod = importlib.import_module(f'{wd}.{key}')
    print(key)
    page = app_to_page(getattr(mod, "app"), id=key, label=label_map[key])
    page.callbacks(app)
    # Render app code.
    with open(code_path, 'r') as f:
        content = f.read()
        # Replace enrich import.
        content = content.replace("from dash_extensions.enrich import DashProxy", "from dash import Dash")
        content = content.replace("DashProxy(", "Dash(")
        # Format as Python code.
        code = dcc.Markdown("````python\n{}\n````".format(content), className="python")
    # Put everything together.
    return elements + [html.Div([page.layout(), code], className="frame")]


def build_content(app):
    content = [html.A(id="home", className="anchor"), html.Br()] + landing_page() + \
              [html.A(id="start", className="anchor"), html.Hr()] + getting_started() + \
              [html.A(id="components", className="anchor"), html.Hr()] + components() + \
              [html.A(id="func_props", className="anchor"), html.Hr()] + func_props() + \
              [html.A(id="examples", className="anchor"), html.Hr()] + examples()
    # Add examples.
    for key in example_keys:
        content += build_example(app, key, example_labels, "examples")
    content += [html.A(id="tutorials", className="anchor"), html.Hr()] + tutorials()
    # Add tutorials.
    for key in tutorial_keys:
        content += build_example(app, key, tutorial_labels, "tutorials")
    return content


def build_navigation():
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
            dbc.NavItem(dbc.NavLink("Functional properties", href="/#func_props", external_link=True)),
            # Example links.
            dbc.NavItem(dbc.NavLink("Examples", href="/#examples", external_link=True,
                                    style={"margin-left": "100px"})),
            dbc.DropdownMenu(
                label="", children=examples_links, in_navbar=True, nav=True, direction="left",
                style={"margin-left": "0px"}),
            # Tutorials links.
            dbc.NavItem(dbc.NavLink("GeoJSON tutorial", href="/#tutorials", external_link=True)),
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
app = Dash(server=server, external_stylesheets=ext_css, external_scripts=ext_js, prevent_initial_callbacks=True)
# Setup layout.
app.layout = html.Div([build_navigation(), dbc.Container(build_content(app), id="content")] +
                      fix_page_load_anchor_issue(app, delay=650))

if __name__ == '__main__':
    app.run_server(port=9999)
