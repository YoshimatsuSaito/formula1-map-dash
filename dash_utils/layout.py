import dash_core_components as dcc
import dash_html_components as html


def get_layout(fig, SEASON):
    """Get the layout of the app."""
    layout = html.Div(
        style={"display": "flex", "flex-direction": "column"},
        children=[
            html.Div(
                style={"height": "18vh"},
                children=[
                    html.H1(f"FIA Formula One World Championship {SEASON}", style={"font-family": "Russo One", "padding": "0px", "margin-bottom": "0px", "margin-left": "5%"}),
                    html.H5("Click a point and see information about the grand prix", style={"font-family": "Russo One", "padding": "0px", "margin-bottom": "0px",  "margin-top": "0px", "margin-left": "5%"})
                ]
            ),
            html.Div(
                style={"display": "flex", "flex-direction": "row", "height": "82vh"},
                children=[
                    dcc.Graph(
                        id="map",
                        config={"displayModeBar": False},
                        figure=fig,
                        style={"height": "100%", "flex": "60%"}
                    ),
                    html.Div(
                        id="hover-data",
                        style={"flex": "40%", "height": "100%"}
                    )
                ]
            ),
            html.Div(
                id="new-div",
                children=[
                    html.Iframe(src="https://en.wikipedia.org/wiki/2023_Austrian_Grand_Prix", style={"height": "100vh", "width": "100vw"}),
                ],
                style={"height": "100vh", "width": "100vw"}
            ),
        ]
    )

    return layout
