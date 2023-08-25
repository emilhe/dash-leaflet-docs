from os import environ

import dash
import dash_mantine_components as dmc
import requests

from dash import html
from dash_down.express import md_to_blueprint_dmc
from dash_iconify import DashIconify
from utils.markdown import python_code
from utils.ui import create_table_of_contents

desc = "Dash Leaflet is a wrapper of Leaflet, the leading open-source JavaScript library for interactive maps."
dash.register_page(
    __name__,
    "/",
    title="Dash Leaflet",
    description=desc,
)


def create_title(title, id):
    return dmc.Text(title, align="center", style={"fontSize": 30}, id=id)


def create_head(text):
    return dmc.Text(text, align="center", my=10, mx=0)


def create_contributors_avatars():
    resp = requests.get(
        "https://api.github.com/repos/thedirtyfew/dash-leaflet/contributors",
        headers={"authorization": f"token {environ['CONTRIB_TOKEN']}"},
    )
    contributors = resp.json()
    children = []
    for user in contributors:
        avatar = dmc.Tooltip(
            dmc.Anchor(dmc.Avatar(src=user["avatar_url"]), href=user["html_url"]),
            label=user["login"],
            position="bottom",
        )
        children.append(avatar)
    return dmc.Group(children, position="center", id="contributors")


md_options = dict(directives=[python_code], dash_proxy_shell=lambda x, y: html.Center(y))
layout = html.Div([
    dmc.Container([
        html.A(id="home", className="anchor"),
        md_to_blueprint_dmc("pages/appetizer.md", **md_options).layout,
        dmc.Space(h=16),
        html.Div(dmc.Divider(), style=dict(width="100%")),
        dmc.Space(h=16),
        html.A(id="quick_start", className="anchor"),
        md_to_blueprint_dmc("pages/quick_start.md", **md_options).layout,
        dmc.Space(h=16),
        html.Div(dmc.Divider(), style=dict(width="100%")),
        dmc.Space(h=16),
        (create_contributors_avatars() if "CONTRIB_TOKEN" in environ else None),
        dmc.Space(h=16),
        html.Div(dmc.Divider(), style=dict(width="100%")),
        dmc.Space(h=16),
        dmc.Center(
            dmc.Group(
                spacing="xs",
                children=[
                    dmc.Text("Made with"),
                    DashIconify(icon="akar-icons:heart", width=19, color="red"),
                    dmc.Text("by Emil Haldrup Eriksen"),
                ],
            )),
    ], fluid=True),
    create_table_of_contents([
        ("#home", "Home", ""),
        ("#quick-start", "Quick start", ""),
        ("#contributors", "Contributors", "")
    ])
])
