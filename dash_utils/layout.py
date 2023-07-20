import os
import sys

import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(os.path.dirname(current_dir), "dash_utils"))

from components import get_number_input


def get_page1_layout(fig, SEASON):
    """Get the layout of page1."""
    return html.Div(
        style={"display": "flex", "flex-direction": "column", "height": "95vh", "overflow": "auto"},
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
        ]
    )


def get_page2_layout(total_laps=50, pitloss=20, soft_pace=90, medium_degradation=0.05):
    """Get the layout of page2"""
    return html.Div(
        style={"display": "flex", "flex-direction": "column", "height": "95vh", "overflow": "auto", "margin-top": "10vh"},
        children=[
            html.Div(
                style={"display": "flex", "justify-content": "center", "align-items": "center", "width": "100%", "height": "15vh"},
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
                        }
                    ),
                ]
            ),
            html.Div(
                id="strategy",
                children=[
                    dbc.Container(fluid=True, style={"margin-bottom": "2%"}, children=[
                        dbc.Row(justify="center", align="center", children=[
                            dbc.Col(html.Label("Total Laps"), xs=3, sm=2, md=2, lg=1, xl=1),
                            dbc.Col(html.Label("Pitloss"), xs=3, sm=2, md=2, lg=1, xl=1),
                        ]),
                        dbc.Row(justify="center", align="center", children=[
                            dbc.Col([get_number_input("Total-Laps", value=total_laps)], xs=3, sm=2, md=2, lg=1, xl=1),
                            dbc.Col([get_number_input("Pitloss", value=pitloss)], xs=3, sm=2, md=2, lg=1, xl=1),
                        ]),
                    ]),
                    dbc.Container(fluid=True, children=[
                        dbc.Row(justify="center", align="center", children=[
                            dbc.Col(html.Div(), xs=3, sm=2, md=2, lg=1, xl=1),
                            dbc.Col(html.Label("Soft"), xs=3, sm=2, md=2, lg=1, xl=1),
                            dbc.Col(html.Label("Medium"), xs=3, sm=2, md=2, lg=1, xl=1),
                            dbc.Col(html.Label("Hard"), xs=3, sm=2, md=2, lg=1, xl=1),
                        ]),
                        dbc.Row(justify="center", align="center", children=[
                            dbc.Col([html.Label("Pace")], xs=3, sm=2, md=2, lg=1, xl=1),
                            dbc.Col([get_number_input("Soft-Pace", value=soft_pace)], xs=3, sm=2, md=2, lg=1, xl=1),
                            dbc.Col([get_number_input("Medium-Pace", value=soft_pace * 1.005)], xs=3, sm=2, md=2, lg=1, xl=1),
                            dbc.Col([get_number_input("Hard-Pace", value=soft_pace * 1.01)], xs=3, sm=2, md=2, lg=1, xl=1),
                        ]),
                        dbc.Row(justify="center", align="center", children=[
                            dbc.Col([html.Label("Degradation")], xs=3, sm=2, md=2, lg=1, xl=1),
                            dbc.Col([get_number_input("Soft-Degradation", value=medium_degradation * 1.01)], xs=3, sm=2, md=2, lg=1, xl=1),
                            dbc.Col([get_number_input("Medium-Degradation", value=medium_degradation)], xs=3, sm=2, md=2, lg=1, xl=1),
                            dbc.Col([get_number_input("Hard-Degradation", value=medium_degradation * 0.99)], xs=3, sm=2, md=2, lg=1, xl=1),
                        ])
                    ])
                ],
                style={
                    "flex-grow": "1",
                    "margin-top": "0%", 
                    "margin-bottom": "3%", 
                    "margin-left": "3%",
                    "margin-right": "3%",
                },
                className="data-content",
            ),
            html.Br(),
            html.Div(
                style={"display": "flex", "justify-content": "center", "align-items": "center", "height": "5vh"},
                children=[dcc.Link("Back to Home", href="/")]
            )
        ]
    )

