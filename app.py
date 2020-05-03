import importlib
import os

import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_leaflet as dl
import dash_core_components as dcc

from flask import Flask


def sz():
    return dict(sm=12, md={"size": 8, "offset": 2})


def render_example(app, key):
    # Render markdown description.
    with open("examples/{}.md".format(key), 'r') as f:
        info = dcc.Markdown(f.read())
    # Render app code.
    with open("examples/{}.py".format(key), 'r') as f:
        code = dcc.Markdown("````\n{}\n````".format(f.read()))
    # TODO: Maybe prefix component IDs? Needs to be BOTH in callback and in
    # Render the example itself.
    class AppProxy:

        def __init__(self):
            self.layout = None

        def callback(self, *args):
            return app.callback(*args)
    # Apply temporary monkey patch.
    dash_real = dash.Dash
    dash.Dash = AppProxy
    mod = importlib.import_module('examples.{}'.format(key))
    example = getattr(mod, "app").layout
    dash.Dash = dash_real
    # TODO: Render example.
    return html.Div([
        dbc.Row(dbc.Col(info)),
        dbc.Row(dbc.Col(example, **sz())),
        dbc.Row(dbc.Col(code))
    ])


# region Elements

def landing_page():
    content = html.Div([
        dcc.Markdown("""Dash Leaflet is a wrapper of [Leaflet](https://leafletjs.com/), the leading open-source 
        JavaScript library for interactive maps. """),
        html.Img(src="assets/leaflet.png", style={"margin": "auto", "display": "block"}),
        dcc.Markdown("""The syntax is similar to other [Dash](https://plotly.com/dash/) components, with naming 
        conventions following [React-Leaflet](https://react-leaflet.js.org/). """)
    ])
    return [dbc.Row(dbc.Col(content, **sz()))]


def getting_started():
    with open("content/getting_started.md", 'r') as f:
        content = f.read()
    example = dl.Map(dl.TileLayer(), style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"})
    return [
        dbc.Row(dbc.Col([dcc.Markdown(content)])),
        dbc.Row(dbc.Col(example, **sz())),
    ]


def components():
    with open("content/components.md", 'r') as f:
        content = f.read()
    return [dbc.Row(dbc.Col([dcc.Markdown(content)]))]


def examples():
    # Load intro.
    with open("content/examples.md", 'r') as f:
        content = f.read()
    rows = [dbc.Row(dbc.Col(dcc.Markdown(content)))]
    # Load examples.
    for key in ["map_click"]:
        rows.append(render_example(app, key))
    return rows


# endregion

def get_content():
    return [html.A(id="home", className="anchor"), html.Br()] + landing_page() + \
           [html.A(id="start", className="anchor"), html.Hr()] + getting_started() + \
           [html.A(id="components", className="anchor"), html.Hr()] + components() + \
           [html.A(id="examples", className="anchor"), html.Hr()] + examples()


def get_nav():
    return dbc.NavbarSimple(
        dbc.Nav([dbc.NavItem(dbc.NavLink("Home", href="#", external_link=True, active=True)),
                 dbc.NavItem(dbc.NavLink("Getting started", href="#start", external_link=True)),
                 dbc.NavItem(dbc.NavLink("Components", href="#components", external_link=True)),
                 dbc.NavItem(dbc.NavLink("Examples", href="#examples", external_link=True))],
                fill=True), fluid=True, sticky="top")


# Create app.
server = Flask(__name__)
app = dash.Dash(server=server, external_stylesheets=[dbc.themes.CERULEAN])
app.layout = html.Div([get_nav(), dbc.Container(get_content())])

if __name__ == '__main__':
    app.run_server(debug=False, port=8051)
