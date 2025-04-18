import dash
import dash_mantine_components as dmc
from dash_extensions import Lottie

dash.register_page(__name__, path="/404")

layout = dmc.Stack(
    align="center",
    children=[
        Lottie(
            options=dict(loop=True, autoplay=True, style=dict(width="40%", margin="auto")),
            url="https://assets5.lottiefiles.com/packages/lf20_kcsr6fcp.json",
        ),
        dmc.Text(
            [
                "If you think this page should exist, create an issue ",
                dmc.Anchor(
                    "here",
                    underline=False,
                    href="https://github.com/thedirtyfew/dash-leaflet/issues/new",
                ),
                ".",
            ]
        ),
        dmc.Anchor("Go back to home ->", href="/", underline=False),
    ],
)
