import dash_core_components as dcc
import dash_html_components as html


def get_layout(fig, SEASON):
    """Get the layout of the app."""
    layout = html.Div(
        style={"display": "flex", "flex-direction": "column"},
        children=[
            html.Div(
                style={"height": "15vh", "margin-bottom": "0px"},
                children=[
                    html.H1(
                        f"FIA Formula One World Championship {SEASON}", 
                        className="my-title",
                        style={
                            "height": "100%", 
                            "font-family": "Russo One", 
                            "margin-top": "3%", 
                            "margin-bottom": "0%", 
                            "margin-left": "3%",
                        }
                    ),
                ]
            ),
            html.Div(
                className="responsive-div",
                style={
                    "display": "flex", 
                    "flex-direction": "row", 
                    "height": "80vh", 
                    "margin-top": "0%", 
                    "margin-bottom": "3%", 
                    "margin-left": "3%",
                    "margin-right": "3%",
                },
                children=[
                    dcc.Graph(
                        id="map",
                        config={"displayModeBar": False},
                        figure=fig,
                        style={
                            "flex": "50%",
                            "height": "100%", 
                            "margin-top": "3%", 
                            "margin-bottom": "3%", 
                            "margin-left": "3%",
                            "margin-right": "3%",
                        }
                    ),
                    html.Div(
                        id="hover-data",
                        style={
                            "flex": "50%", 
                            "height": "100%",
                            "margin-top": "3%", 
                            "margin-bottom": "3%", 
                            "margin-left": "3%",
                            "margin-right": "3%",
                        }
                    )
                ]
            ),
            # html.Div(
            #     id="new-div",
            #     children=[
            #         html.Iframe(src="https://en.wikipedia.org/wiki/2023_Austrian_Grand_Prix", style={"height": "100vh", "width": "100vw"}),
            #     ],
            #     style={"height": "100vh", "width": "100vw"}
            # ),
        ]
    )

    return layout
