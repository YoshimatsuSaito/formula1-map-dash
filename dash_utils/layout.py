import os
import sys

import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(os.path.dirname(current_dir), "dash_utils"))

from components import get_number_input
from plotting import create_prediction_figure


def get_page1_layout(fig, SEASON):
    """Get the layout of page1."""
    return html.Div(
        style={
            "display": "flex",
            "flex-direction": "column",
            "height": "95vh",
            "overflow": "auto",
        },
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
                        },
                    ),
                ],
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
                        },
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
                        },
                    ),
                ],
            ),
        ],
    )


def get_page2_layout(totallap=50, pitloss=20, medium_pace=90, medium_degradation=0.05):
    """Get the layout of page2"""
    if totallap == 999:
        totallap = None
    if pitloss == 999:
        pitloss = None
    if medium_pace == 999:
        soft_pace, medium_pace, hard_pace = None, None, None
    else:
        soft_pace = round(medium_pace * 0.99, 3)
        hard_pace = round(medium_pace * 1.02, 3)
    if medium_degradation == 999:
        soft_degradation, medium_degradation, hard_degradation = None, None, None
    else:
        abs_medium_degradation = abs(medium_degradation)
        if medium_degradation >= 0:
            soft_degradation = medium_degradation * 2
            hard_degradation = medium_degradation / 2
        else:
            soft_degradation = medium_degradation + abs_medium_degradation * 2
            hard_degradation = medium_degradation - abs_medium_degradation / 2
        soft_degradation = round(soft_degradation, 3)
        hard_degradation = round(hard_degradation, 3)
    return html.Div(
        style={
            "display": "flex",
            "flex-direction": "column",
            "height": "160vh",
            "overflow": "auto",
            "margin-top": "10vh",
            "justify-content": "center",
        },
        children=[
            html.Div(
                style={
                    "display": "flex",
                    "justify-content": "center",
                    "align-items": "center",
                    "width": "100%",
                    "height": "15vh",
                },
                children=[
                    html.H1(
                        "Strategy simulator",
                        className="my-title",
                        style={
                            "height": "100%",
                            "font-family": "Russo One",
                            "margin-top": "3%",
                            "margin-bottom": "0%",
                            "margin-left": "3%",
                        },
                    ),
                ],
            ),
            html.Div(
                id="strategy",
                children=[
                    dbc.Container(
                        fluid=True,
                        style={"margin-bottom": "2%"},
                        children=[
                            dbc.Row(
                                justify="center",
                                align="center",
                                children=[
                                    dbc.Col(
                                        html.Label("Total Laps"),
                                        xs=3,
                                        sm=2,
                                        md=2,
                                        lg=1,
                                        xl=1,
                                    ),
                                    dbc.Col(
                                        html.Label("Pitloss"),
                                        xs=3,
                                        sm=2,
                                        md=2,
                                        lg=1,
                                        xl=1,
                                    ),
                                ],
                            ),
                            dbc.Row(
                                justify="center",
                                align="center",
                                children=[
                                    dbc.Col(
                                        [
                                            get_number_input(
                                                "Total-Laps", value=totallap
                                            )
                                        ],
                                        xs=3,
                                        sm=2,
                                        md=2,
                                        lg=1,
                                        xl=1,
                                    ),
                                    dbc.Col(
                                        [get_number_input("Pitloss", value=pitloss)],
                                        xs=3,
                                        sm=2,
                                        md=2,
                                        lg=1,
                                        xl=1,
                                    ),
                                ],
                            ),
                        ],
                    ),
                    dbc.Container(
                        fluid=True,
                        children=[
                            dbc.Row(
                                justify="center",
                                align="center",
                                children=[
                                    dbc.Col(html.Div(), xs=3, sm=2, md=2, lg=1, xl=1),
                                    dbc.Col(
                                        html.Label("Soft"), xs=3, sm=2, md=2, lg=1, xl=1
                                    ),
                                    dbc.Col(
                                        html.Label("Medium"),
                                        xs=3,
                                        sm=2,
                                        md=2,
                                        lg=1,
                                        xl=1,
                                    ),
                                    dbc.Col(
                                        html.Label("Hard"), xs=3, sm=2, md=2, lg=1, xl=1
                                    ),
                                ],
                            ),
                            dbc.Row(
                                justify="center",
                                align="center",
                                children=[
                                    dbc.Col(
                                        [html.Label("Pace")],
                                        xs=3,
                                        sm=2,
                                        md=2,
                                        lg=1,
                                        xl=1,
                                    ),
                                    dbc.Col(
                                        [
                                            get_number_input(
                                                "Soft-Pace", value=soft_pace
                                            )
                                        ],
                                        xs=3,
                                        sm=2,
                                        md=2,
                                        lg=1,
                                        xl=1,
                                    ),
                                    dbc.Col(
                                        [
                                            get_number_input(
                                                "Medium-Pace", value=medium_pace
                                            )
                                        ],
                                        xs=3,
                                        sm=2,
                                        md=2,
                                        lg=1,
                                        xl=1,
                                    ),
                                    dbc.Col(
                                        [
                                            get_number_input(
                                                "Hard-Pace", value=hard_pace
                                            )
                                        ],
                                        xs=3,
                                        sm=2,
                                        md=2,
                                        lg=1,
                                        xl=1,
                                    ),
                                ],
                            ),
                            dbc.Row(
                                justify="center",
                                align="center",
                                children=[
                                    dbc.Col(
                                        [html.Label("Degradation")],
                                        xs=3,
                                        sm=2,
                                        md=2,
                                        lg=1,
                                        xl=1,
                                    ),
                                    dbc.Col(
                                        [
                                            get_number_input(
                                                "Soft-Degradation",
                                                value=soft_degradation,
                                            )
                                        ],
                                        xs=3,
                                        sm=2,
                                        md=2,
                                        lg=1,
                                        xl=1,
                                    ),
                                    dbc.Col(
                                        [
                                            get_number_input(
                                                "Medium-Degradation",
                                                value=medium_degradation,
                                            )
                                        ],
                                        xs=3,
                                        sm=2,
                                        md=2,
                                        lg=1,
                                        xl=1,
                                    ),
                                    dbc.Col(
                                        [
                                            get_number_input(
                                                "Hard-Degradation",
                                                value=hard_degradation,
                                            )
                                        ],
                                        xs=3,
                                        sm=2,
                                        md=2,
                                        lg=1,
                                        xl=1,
                                    ),
                                ],
                            ),
                        ],
                    ),
                    html.Div(
                        html.Button(
                            "Simulate strategy",
                            id="run-simulation-button",
                            n_clicks=0,
                            style={
                                "borderRadius": "15px",
                                "backgroundColor": "rgb(173, 255, 47)",
                                "border": "2px solid rgb(0, 0, 0)",
                                "color": "black",
                            },
                        ),
                        style={
                            "textAlign": "center",
                            "margin-top": "3%",
                            "margin-bottom": "0%",
                        },
                    ),
                ],
                style={
                    "flex-grow": "1",
                    "margin-top": "0%",
                    "margin-bottom": "3%",
                    "margin-left": "3%",
                    "margin-right": "3%",
                    "justify-content": "center",
                    "align-items": "center",
                },
                className="data-content",
            ),
            html.Div(
                children=[
                    dcc.Graph(
                        id="simulation-results",
                        config={"displayModeBar": False},
                        figure={},
                        style={
                            "justify-content": "center",
                            "align-items": "center",
                            "textAlign": "center",
                            "height": "100%",
                            "width": "80%",
                        },
                    ),
                ],
                style={
                    "display": "flex",
                    "justify-content": "center",
                    "align-items": "center",
                    "textAlign": "center",
                    "height": "80vh",
                    "width": "100%",
                    "margin-bottom": "3%",
                },
            ),
            html.Br(),
            html.Div(
                style={
                    "display": "flex",
                    "justify-content": "center",
                    "align-items": "center",
                    "height": "5vh",
                },
                children=[dcc.Link("Back to Home", href="/")],
            ),
        ],
    )


def get_page3_layout(gp_name, df_prediction):
    """Get the layout of page3"""
    return html.Div(
        style={
            "display": "flex",
            "flex-direction": "column",
            "height": "95vh",
            "overflow": "auto",
        },
        children=[
            html.Div(
                style={
                    "display": "flex",
                    "justify-content": "center",
                    "align-items": "center",
                    "width": "100%",
                    "height": "15vh",
                },
                children=[
                    html.H1(
                        f"Prediction of {gp_name}",
                        className="my-title",
                        style={
                            "height": "100%",
                            "font-family": "Russo One",
                            "margin-top": "3%",
                            "margin-bottom": "0%",
                            "margin-left": "3%",
                        },
                    ),
                ],
            ),
            html.Div(
                id="prediction-result",
                children=[
                    dcc.Graph(
                        figure=create_prediction_figure(df_prediction),
                        config={"displayModeBar": False},
                        style={
                            "flex": "50%",
                            "height": "100%",
                            "margin-top": "3%",
                            "margin-bottom": "3%",
                            "margin-left": "3%",
                            "margin-right": "3%",
                        },
                    ),
                ],
                style={
                    "display": "flex",
                    "justify-content": "center",
                    "align-items": "center",
                    "textAlign": "center",
                    "height": "70vh",
                    "width": "100%",
                    "margin-bottom": "3%",
                },
            ),
            html.Br(),
            html.Div(
                style={
                    "display": "flex",
                    "justify-content": "center",
                    "align-items": "center",
                    "height": "5vh",
                },
                children=[dcc.Link("Back to Home", href="/")],
            ),
        ],
    )
