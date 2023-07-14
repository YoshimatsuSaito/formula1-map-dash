import os
import sys

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(os.path.dirname(current_dir), "dash_utils"))

from components import get_number_input


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
            html.Div(
                id="strategy",
                children=[
                    dbc.Container(fluid=True, children=[
                        dbc.Row(children=[
                            dbc.Col(html.Div(), width=2),
                            dbc.Col(html.Label("Soft"), width=2),
                            dbc.Col(html.Label("Medium"), width=2),
                            dbc.Col(html.Label("Hard"), width=2),
                        ]),
                        dbc.Row(children=[
                            dbc.Col(html.Label("Pace"), width=2),
                            dbc.Col([get_number_input("Soft-Pace")], width=2),
                            dbc.Col([get_number_input("Medium-Pace")], width=2),
                            dbc.Col([get_number_input("Hard-Pace")], width=2),
                        ]),
                        dbc.Row(children=[
                            dbc.Col(html.Label("Degradation"), width=2),
                            dbc.Col([get_number_input("Soft-Degradation")], width=2),
                            dbc.Col([get_number_input("Medium-Degradation")], width=2),
                            dbc.Col([get_number_input("Hard-Degradation")], width=2),
                        ])
                    ])
                ],
                style={"height": "30vh"}
            ),
        ]
    )

    return layout

