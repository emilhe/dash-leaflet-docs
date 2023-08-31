import dash_leaflet
import dash_mantine_components as dmc
from collections import defaultdict
from dash_iconify import DashIconify
from dash_extensions.enrich import dcc, html, page_container, clientside_callback, Output, Input, State


def create_icon_section_label(label: str, icon: str, labelPosition: str = "left", my="sm") -> dmc.Divider:
    return dmc.Divider(
        labelPosition=labelPosition,
        label=[
            DashIconify(
                icon=f"radix-icons:{icon}", width=15, style={"marginRight": 10}
            ), label
        ],
        my=my,
    )


IGNORE_SECTIONS = ["Content", "Pages"]
HOME = f"Dash Leaflet"
HOME_SHORT = "DL"
BADGE = dash_leaflet.__version__
GITHUB_URL = "https://github.com/thedirtyfew/dash-leaflet"
COMPONENT_CATEGORIES = ["Ui Layers", "Raster Layers", "Vector Layers", "Controls", "Misc"]
SECTION_LABELS = {
    "Components": create_icon_section_label("Component API Reference", "component-1", my=10, labelPosition="right"),
    "Components/Ui Layers": create_icon_section_label("UI Layers", "eye-open"),
    "Components/Controls": create_icon_section_label("Controls", "gear"),
    "Components/Misc": create_icon_section_label("Misc", "mix"),
    "Components/Vector Layers": create_icon_section_label("Vector Layers", "angle"),
    "Components/Raster Layers": create_icon_section_label("Raster Layers", "image"),
}


# region Sourced from dmc docs: https://github.com/snehilvj/dmc-docs/blob/main/lib/appshell.py

def create_home_link(label: str) -> dmc.Anchor:
    return dmc.Anchor(
        label,
        size="xl",
        href="/",
        underline=False,
    )


def create_main_nav_link(icon: str, label: str, href: str) -> dmc.Anchor:
    return dmc.Anchor(
        dmc.Group(
            [
                DashIconify(
                    icon=icon, width=23, color=dmc.theme.DEFAULT_COLORS["indigo"][5]
                ),
                dmc.Text(label, size="sm"),
            ]
        ),
        href=href,
        variant="text",
    )


def create_header_link(icon: str, href: str, size: int = 22, color: str = "indigo") -> dmc.Anchor:
    return dmc.Anchor(
        dmc.ThemeIcon(
            DashIconify(
                icon=icon,
                width=size,
            ),
            variant="outline",
            radius=30,
            size=36,
            color=color,
        ),
        href=href,
        target="_blank",
    )


def create_header(nav_data) -> dmc.Header:
    return dmc.Header(
        height=70,
        fixed=True,
        px=25,
        children=[
            dmc.Stack(
                justify="center",
                style={"height": 70},
                children=dmc.Grid(
                    children=[
                        dmc.Col(
                            [
                                dmc.MediaQuery(
                                    dmc.Group([
                                        create_home_link(HOME), dmc.Badge(
                                            BADGE,
                                            variant="outline",
                                            radius="xl",
                                        )]),
                                    smallerThan="sm",
                                    styles={"display": "none"},
                                ),
                                dmc.MediaQuery(
                                    create_home_link(HOME_SHORT),
                                    largerThan="sm",
                                    styles={"display": "none"},
                                ),
                            ],
                            span="content",
                            pt=12,
                        ),
                        dmc.Col(
                            span="auto",
                            children=dmc.Group(
                                position="right",
                                # spacing="xl",
                                children=[
                                    dmc.Select(
                                        id="select-component",
                                        style={"width": 200},
                                        placeholder="Search",
                                        nothingFound="No match found",
                                        searchable=True,
                                        clearable=True,
                                        data=[
                                            {
                                                "label": component["name"],
                                                "value": component["path"],
                                            }
                                            for component in nav_data
                                            if component["name"]
                                               not in ["Home", "Not found 404"]
                                        ],
                                        icon=DashIconify(
                                            icon="radix-icons:magnifying-glass"
                                        ),
                                    ),
                                    dmc.MediaQuery(
                                        create_header_link(
                                            "radix-icons:github-logo",
                                            GITHUB_URL,
                                        ),
                                        smallerThan="sm",
                                        styles={"display": "none"},
                                    ),
                                    dmc.ActionIcon(
                                        DashIconify(
                                            icon="radix-icons:blending-mode", width=22
                                        ),
                                        variant="outline",
                                        radius=30,
                                        size=36,
                                        color="yellow",
                                        id="color-scheme-toggle",
                                    ),
                                    dmc.MediaQuery(
                                        dmc.MediaQuery(
                                            dmc.ActionIcon(
                                                DashIconify(
                                                    icon="radix-icons:hamburger-menu",
                                                    width=18,
                                                ),
                                                id="drawer-hamburger-button",
                                                variant="outline",
                                                size=36,
                                            ),
                                            largerThan="lg",
                                            styles={"display": "none"},
                                        ),
                                        smallerThan="sm",
                                        styles={"display": "none"},
                                    )
                                ],
                            ),
                        ),
                    ],
                ),
            )
        ],
    )


# NB: Heavily customized
def create_side_nave_content(nav_data) -> dmc.Stack:
    # Setup docs links.
    main_links = dmc.Stack(
        spacing="sm",
        mt=20,
        children=[
            create_main_nav_link(
                icon="material-symbols:rocket-launch-rounded",
                label="Getting Started",
                href="/docs/getting_started",
            ),
            # create_main_nav_link(
            #     icon="material-symbols:apps",
            #     label="Components",
            #     href="/docs/components",
            # ),
            create_main_nav_link(
                icon="material-symbols:magic-button",
                label="Functional Properties",
                href="/docs/func_props",
            ),
            create_main_nav_link(
                icon="material-symbols:event",
                label="Events",
                href="/docs/events",
            ),
            create_main_nav_link(
                icon="material-symbols:target",
                label="GeoJSON Tutorial",
                href="/docs/geojson_tutorial",
            ),
            create_main_nav_link(
                icon="material-symbols:chip-extraction",
                label="Migration",
                href="/docs/migration",
            ),
            # create_main_nav_link(
            #     icon="material-symbols:bug-report",
            #     label="Known issues",
            #     href="/docs/migration",
            # ),
        ],
    )
    # Create component links.
    sections = defaultdict(list)
    for entry in nav_data:
        label = entry["module"].split(".")[0]
        label = (" ".join(label.split("_"))).title()
        if label.startswith("Components"):
            sections[label].append((entry["name"], entry["path"]))
    # Create component main section.
    links = []
    for label in ["Components"] + [f"Components/{c}" for c in COMPONENT_CATEGORIES]:
        items = sections[label]
        links.append(SECTION_LABELS[label])
        links.extend(
            [
                dmc.Anchor(name, size="sm", href=path, variant="text")
                for name, path in items
            ]
        )

    return dmc.Stack(
        spacing="0.3rem", children=[main_links, *links], px=25
    )


def create_side_navbar(nav_data) -> dmc.Navbar:
    return dmc.Navbar(
        fixed=True,
        id="components-navbar",
        position={"top": 70},
        width={"base": 300},
        children=[
            dmc.ScrollArea(
                offsetScrollbars=True,
                type="scroll",
                children=create_side_nave_content(nav_data),
            )
        ],
    )


def create_navbar_drawer(nav_data) -> dmc.Drawer:
    return dmc.Drawer(
        id="components-navbar-drawer",
        overlayOpacity=0.55,
        overlayBlur=3,
        zIndex=9,
        size=300,
        children=[
            dmc.ScrollArea(
                offsetScrollbars=True,
                type="scroll",
                style={"height": "100%"},
                pt=20,
                children=create_side_nave_content(nav_data),
            )
        ],
    )


def create_table_of_contents(toc_items) -> dmc.Aside:
    children = []
    for url, name, _ in toc_items:
        children.append(
            html.A(
                dmc.Text(name, color="dimmed", size="sm", variant="text"),
                style={"textTransform": "capitalize", "textDecoration": "none"},
                href=url,
            )
        )

    heading = dmc.Text("Table of Contents", mb=10, weight=500)
    toc = dmc.Stack([heading, *children], spacing=4, px=25, mt=20)

    return dmc.Aside(
        position={"top": 70, "right": 0},
        fixed=True,
        className="toc-navbar",
        width={"base": 300},
        zIndex=10,
        children=toc,
        withBorder=False,
    )


def create_app_shell(nav_data, children) -> dmc.MantineProvider:
    clientside_callback(
        """ function(data) { return data } """,
        Output("mantine-docs-theme-provider", "theme"),
        Input("theme-store", "data"),
    )

    clientside_callback(
        """function(n_clicks, data) {
            if (data) {
                if (n_clicks) {
                    const scheme = data["colorScheme"] == "dark" ? "light" : "dark"
                    return { colorScheme: scheme } 
                }
                return dash_clientside.no_update
            } else {
                return { colorScheme: "light" }
            }
        }""",
        Output("theme-store", "data"),
        Input("color-scheme-toggle", "n_clicks"),
        State("theme-store", "data"),
    )

    # noinspection PyProtectedMember
    clientside_callback(
        """ function(children) { return null } """,
        Output("select-component", "value"),
        Input("_pages_content", "children"),
    )

    clientside_callback(
        """
        function(value) {
            if (value) {
                return value
            }
        }
        """,
        Output("url", "pathname"),
        Input("select-component", "value"),
    )

    clientside_callback(
        """function(n_clicks) { return true }""",
        Output("components-navbar-drawer", "opened"),
        Input("drawer-hamburger-button", "n_clicks"),
        prevent_initial_call=True,
    )

    return dmc.MantineProvider(
        dmc.MantineProvider(
            theme={
                "fontFamily": "'Inter', sans-serif",
                "primaryColor": "indigo",
                "components": {
                    "Button": {"styles": {"root": {"fontWeight": 400}}},
                    "Alert": {"styles": {"title": {"fontWeight": 500}}},
                    "AvatarGroup": {"styles": {"truncated": {"fontWeight": 500}}},
                },
            },
            inherit=True,
            children=[
                         dcc.Store(id="theme-store", storage_type="local"),
                         dcc.Location(id="url"),
                         html.Div(
                             [
                                 create_header(nav_data),
                                 create_side_navbar(nav_data),
                                 create_navbar_drawer(nav_data),
                                 html.Div(
                                     dmc.Container(size="lg", pt=90, children=page_container),
                                     id="wrapper",
                                 ),
                             ]
                         ),
                     ] + children,
        ),
        theme={"colorScheme": "light"},
        id="mantine-docs-theme-provider",
        withGlobalStyles=True,
        withNormalizeCSS=True,
    )

# endregion

def fix_page_load_anchor_issue(app, delay, input_id=None, output_id=None):
    """
    Fixes the issue that the pages is not scrolled to the anchor position on initial load.
    :param app: the Dash app object
    :param delay: in some cases, an additional delay might be needed for the page to load, specify in ms
    :param input_id: id of input dummy element
    :param output_id: id of output dummy element
    :return: dummy elements, which must be added to the layout for the fix to work
    """
    # Create dummy components.
    input_id = input_id if input_id is not None else "fix_page_load_anchor_issue_input"
    output_id = output_id if output_id is not None else "fix_page_load_anchor_issue_output"
    dummy_input = html.Div(id=input_id, style={"display": "hidden"})
    dummy_output = html.Div(id=output_id, style={"display": "hidden"})
    # Setup the callback that does the magic.
    app.clientside_callback(
        """
        function(dummy_value) {{
            setTimeout(function(){{
                const match = document.getElementById(window.location.hash.substring(1))
                if(match){{match.scrollIntoView();}}
            }}, {});
        }}
        """.format(
            delay
        ),
        Output(output_id, "children"),
        [Input(input_id, "children")],
        prevent_initial_call=False,
    )
    return [dummy_input, dummy_output]