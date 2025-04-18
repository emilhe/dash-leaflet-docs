from collections import defaultdict

import dash_leaflet
import dash_mantine_components as dmc
from dash_extensions.enrich import ALL, Input, Output, State, clientside_callback, dcc, html, page_container
from dash_iconify import DashIconify


def create_icon_section_label(label: str, icon: str, labelPosition: str = "left", my="sm") -> dmc.Divider:
    return dmc.Divider(
        labelPosition=labelPosition,
        label=[DashIconify(icon=f"radix-icons:{icon}", width=15, style={"marginRight": 10}), label],
        my=my,
    )


PRIMARY_COLOR = "blue"
IGNORE_SECTIONS = ["Content", "Pages"]
HOME_SHORT = "DL"
HOME_LONG = "Dash Leaflet"
BADGE = dash_leaflet.__version__
GITHUB_URL = "https://github.com/emilhe/dash-extensions"
COMPONENT_CATEGORIES = ["Ui Layers", "Raster Layers", "Vector Layers", "Controls", "Misc"]
SECTION_LABELS = {
    "Components": create_icon_section_label("Component API Reference", "component-1", my=10, labelPosition="right"),
    "Components/Ui Layers": create_icon_section_label("UI Layers", "eye-open"),
    "Components/Controls": create_icon_section_label("Controls", "gear"),
    "Components/Misc": create_icon_section_label("Misc", "mix"),
    "Components/Vector Layers": create_icon_section_label("Vector Layers", "angle"),
    "Components/Raster Layers": create_icon_section_label("Raster Layers", "image"),
}
NAVLINK_NAVBAR = "navlink_navbar"
NAVLINK_DRAWER = "navlink_drawer"

# region Sourced from dmc docs: https://github.com/snehilvj/dmc-docs/blob/main/lib/appshell.py

# region TOC


def create_table_of_contents(toc_items):
    children = []
    for url, name, _ in toc_items:
        children.append(
            html.A(
                dmc.Text(name, c="dimmed", size="sm", variant="text"),
                style={"textTransform": "capitalize", "textDecoration": "none"},
                href=url,
            )
        )

    heading = dmc.Text("Table of Contents", mb=10, w=500)
    toc = dmc.Stack([heading, *children], gap=4, px=25, mt=20)

    return dmc.AppShellAside(
        pos={"top": 70, "right": 0},
        className="toc-navbar",
        zIndex=10,
        children=toc,
        withBorder=False,
    )


# endregion

# region Navbar


def create_main_link(icon, label, href, idtype) -> dmc.NavLink:
    return dmc.NavLink(
        leftSection=DashIconify(
            icon=icon,
            width=23,
            color=dmc.DEFAULT_THEME["colors"][PRIMARY_COLOR][6],
        ),
        label=label,
        href=href,
        id={"type": idtype, "index": href},
    )


# NB: Heavily customized
def create_content(data, idtype):
    # Setup docs links.
    main_links = dmc.Stack(
        gap=0,
        mt=20,
        children=[
            create_main_link(
                icon="material-symbols:rocket-launch-rounded",
                label="Getting Started",
                href="/docs/getting_started",
                idtype=idtype,
            ),
            create_main_link(
                icon="material-symbols:globe",
                label="Component Overview",
                href="/docs/component_overview",
                idtype=idtype,
            ),
            create_main_link(
                icon="material-symbols:magic-button",
                label="Functional Properties",
                href="/docs/func_props",
                idtype=idtype,
            ),
            create_main_link(
                icon="material-symbols:event",
                label="Events",
                href="/docs/events",
                idtype=idtype,
            ),
            create_main_link(
                icon="material-symbols:target",
                label="GeoJSON Tutorial",
                href="/docs/geojson_tutorial",
                idtype=idtype,
            ),
            create_main_link(
                icon="material-symbols:chip-extraction",
                label="Migration",
                href="/docs/migration",
                idtype=idtype,
            ),
        ],
    )

    # Create component links.
    sections = defaultdict(list)
    for entry in data:
        label = entry["module"].split(".")[0]
        label = (" ".join(label.split("_"))).title()
        sections[label].append((entry["name"], entry["path"]))

    # Create component main section.
    links = []
    for label in ["Components"] + [f"Components/{c}" for c in COMPONENT_CATEGORIES]:
        items = sections[label]
        links.append(SECTION_LABELS[label])
        links.extend(
            [
                dmc.NavLink(
                    label=name,
                    href=path,
                    h=32,
                    className="navbar-link",
                    pl=30,
                    id={"type": idtype, "index": path},
                )
                for name, path in items
            ]
        )

    return dmc.ScrollArea(
        offsetScrollbars=True,
        type="scroll",
        style={"height": "100%"},
        children=dmc.Stack(gap=0, children=[main_links, *links], px=25),
    )


def create_navbar_drawer(data):
    clientside_callback(
        """function(pathname) {
            const lists = dash_clientside.callback_context.states_list;
            const active = lists.map(l => l.map(i => i["id"]["index"] === pathname));
            return active;
        }""",
        Output({"type": NAVLINK_NAVBAR, "index": ALL}, "active"),
        Output({"type": NAVLINK_DRAWER, "index": ALL}, "active"),
        Input("_pages_location", "pathname"),
        State({"type": NAVLINK_NAVBAR, "index": ALL}, "id"),
        State({"type": NAVLINK_DRAWER, "index": ALL}, "id"),
    )

    return dmc.Drawer(
        id="components-navbar-drawer",
        overlayProps={"opacity": 0.55, "blur": 3},
        offset=10,
        radius="md",
        withCloseButton=False,
        size="75%",
        children=create_content(data, NAVLINK_DRAWER),
        trapFocus=False,
    )


def create_navbar(data):
    return dmc.AppShellNavbar(children=create_content(data, NAVLINK_NAVBAR))


# endregion

# region Header


def create_link(icon, href):
    return dmc.Anchor(
        dmc.ActionIcon(DashIconify(icon=icon, width=25), variant="transparent", size="lg"),
        href=href,
        target="_blank",
        visibleFrom="xs",
    )


def create_version_menu() -> dmc.Badge:
    return dmc.Badge(
        BADGE,
        variant="filled",
        radius="xl",
    )


def create_search(data):
    return dmc.Select(
        id="select-component",
        placeholder="Search",
        mt=-2,
        searchable=True,
        clearable=True,
        w=250,
        nothingFoundMessage="Nothing Found!",
        leftSection=DashIconify(icon="mingcute:search-3-line"),
        data=[
            {"label": component["name"], "value": component["path"]}
            for component in data
            if component["name"] not in ["Home", "Not found 404"]
        ],
        visibleFrom="sm",
        comboboxProps={"shadow": "md"},
    )


def create_header(data):
    clientside_callback(
        """
        function(value) { 
            if (value) {
                return value
            }
        }
        """,
        Output("url", "href"),
        Input("select-component", "value"),
    )

    clientside_callback(
        """function(n_clicks) { return true }""",
        Output("components-navbar-drawer", "opened"),
        Input("drawer-hamburger-button", "n_clicks"),
        prevent_initial_call=True,
    )

    return dmc.AppShellHeader(
        px=25,
        children=[
            dmc.Stack(
                justify="center",
                h=70,
                children=dmc.Grid(
                    justify="space-between",
                    children=[
                        dmc.GridCol(
                            dmc.Group(
                                [
                                    dmc.Anchor(
                                        HOME_LONG,
                                        size="xl",
                                        href="/",
                                        underline=False,
                                        pb=3,
                                        visibleFrom="lg",
                                    ),
                                    dmc.Anchor(
                                        HOME_SHORT,
                                        size="xl",
                                        href="/",
                                        underline=False,
                                        pb=3,
                                        hiddenFrom="lg",
                                    ),
                                    create_version_menu(),
                                ]
                            ),
                            span="content",
                        ),
                        dmc.GridCol(
                            span="auto",
                            children=dmc.Group(
                                justify="flex-end",
                                h=31,
                                gap="xl",
                                children=[
                                    create_search(data),
                                    create_link(
                                        "radix-icons:github-logo",
                                        GITHUB_URL,
                                    ),
                                    dmc.ActionIcon(
                                        [
                                            DashIconify(
                                                icon="radix-icons:sun",
                                                width=25,
                                                id="light-theme-icon",
                                            ),
                                            DashIconify(
                                                icon="radix-icons:moon",
                                                width=25,
                                                id="dark-theme-icon",
                                            ),
                                        ],
                                        variant="transparent",
                                        color="yellow",
                                        id="color-scheme-toggle",
                                        size="lg",
                                    ),
                                    dmc.ActionIcon(
                                        DashIconify(
                                            icon="radix-icons:hamburger-menu",
                                            width=25,
                                        ),
                                        id="drawer-hamburger-button",
                                        variant="transparent",
                                        size="lg",
                                        hiddenFrom="lg",
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            )
        ],
    )


# endregion

# region App shell


def create_app_shell(data, children):
    clientside_callback(
        "function(colorScheme) {return colorScheme}",
        Output("m2d-mantine-provider", "forceColorScheme"),
        Input("color-scheme-storage", "data"),
    )

    clientside_callback(
        'function(n_clicks, theme) {return theme === "dark" ? "light" : "dark"}',
        Output("color-scheme-storage", "data"),
        Input("color-scheme-toggle", "n_clicks"),
        State("color-scheme-storage", "data"),
        prevent_initial_call=True,
    )

    return dmc.MantineProvider(
        id="m2d-mantine-provider",
        forceColorScheme="light",
        theme={
            "primaryColor": PRIMARY_COLOR,
            # "fontFamily": "'Inter', sans-serif",
            "components": {
                "Button": {"defaultProps": {"fw": 400}},
                "Alert": {"styles": {"title": {"fontWeight": 500}}},
                "AvatarGroup": {"styles": {"truncated": {"fontWeight": 500}}},
                "Badge": {"styles": {"root": {"fontWeight": 500}}},
                "Progress": {"styles": {"label": {"fontWeight": 500}}},
                "RingProgress": {"styles": {"label": {"fontWeight": 500}}},
                "CodeHighlightTabs": {"styles": {"file": {"padding": 12}}},
                "Table": {
                    "defaultProps": {
                        "highlightOnHover": True,
                        "withTableBorder": True,
                        "verticalSpacing": "sm",
                        "horizontalSpacing": "md",
                    }
                },
            },
            "colors": {
                "myColor": [
                    "#F2FFB6",
                    "#DCF97E",
                    "#C3E35B",
                    "#AAC944",
                    "#98BC20",
                    "#86AC09",
                    "#78A000",
                    "#668B00",
                    "#547200",
                    "#455D00",
                ]
            },
        },
        children=[
            dcc.Location(id="url", refresh="callback-nav"),
            dcc.Store(id="color-scheme-storage", storage_type="local"),
            dmc.NotificationProvider(),
            dmc.AppShell(
                [
                    create_header(data),
                    create_navbar(data),
                    create_navbar_drawer(data),
                    dmc.AppShellMain(children=page_container),
                ],
                header={"height": 70},
                padding="xl",
                navbar={
                    "width": 300,
                    "breakpoint": "lg",
                    "collapsed": {"mobile": True},
                },
                aside={
                    "width": 300,
                    "breakpoint": "xl",
                    "collapsed": {"desktop": False, "mobile": True},
                },
            ),
        ]
        + children,
    )


# endregion

# endregion
