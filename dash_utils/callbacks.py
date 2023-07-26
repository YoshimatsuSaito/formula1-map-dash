import json
import os
import sys

import dash
import urllib
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(os.path.dirname(current_dir), "dash_utils"))
sys.path.append(os.path.join(os.path.dirname(current_dir), "modules"))

from plotting import create_circuit_figure, create_main_figure, create_strategy_figure
from strategy_maker import optimize_strategy


def register_page1_callbacks(app, data4app):
    """Register callbacks for the page1"""

    @app.callback(
        Output("map_circuit", "figure"),
        [Input("map-style-radio", "value"), Input("map", "clickData")],
    )
    def update_circuit_figure(map_style="streets", clickData=None):
        """Update the circuit figure."""
        if clickData is None:
            clickData = data4app.default_clickdata
        fig_circuit = create_circuit_figure(
            data4app.latest_gp_index, data4app.df, map_style, clickData
        )
        return fig_circuit

    @app.callback(
        Output("hover-data", "children"),
        [Input("map", "clickData")],
    )
    def update_hover_data(clickData):
        """Update hover (click) data"""
        if clickData is None:
            clickData = data4app.default_clickdata

        fp1 = clickData["points"][0]["customdata"]["fp1"]
        fp2 = clickData["points"][0]["customdata"]["fp2"]
        fp3 = clickData["points"][0]["customdata"]["fp3"]
        qualifying = clickData["points"][0]["customdata"]["qualifying"]
        sprint = clickData["points"][0]["customdata"]["sprint"]
        race = clickData["points"][0]["customdata"]["race"]
        gp_name = clickData["points"][0]["customdata"]["gp_name"]
        url = clickData["points"][0]["customdata"]["url"]
        circuit = clickData["points"][0]["customdata"]["circuit"]
        return [
            html.Div(
                [
                    html.Div(
                        f"{gp_name}",
                        style={"font-family": "Russo One", "height": "4%"},
                        className="data-content",
                    ),
                    html.Div(
                        f"Circuit: {circuit}",
                        style={"font-family": "Russo One", "height": "4%"},
                        className="data-content",
                    ),
                    html.Div(
                        f"FP1: {fp1}",
                        style={"font-family": "Russo One", "height": "4%"},
                        className="data-content",
                    ),
                    html.Div(
                        f"FP2: {fp2}",
                        style={"font-family": "Russo One", "height": "4%"},
                        className="data-content",
                    ),
                    html.Div(
                        f"FP3: {fp3}",
                        style={"font-family": "Russo One", "height": "4%"},
                        className="data-content",
                    ),
                    html.Div(
                        f"Qualifying: {qualifying}",
                        style={"font-family": "Russo One", "height": "4%"},
                        className="data-content",
                    ),
                    html.Div(
                        f"Sprint: {sprint}",
                        style={"font-family": "Russo One", "height": "4%"},
                        className="data-content",
                    ),
                    html.Div(
                        f"Race: {race}",
                        style={"font-family": "Russo One", "height": "4%"},
                        className="data-content",
                    ),
                    dcc.Link(
                        "View Predictions / Results",
                        href="/Prediction",
                        style={"height": "4%"},
                    ),
                    html.Br(),
                    dcc.Link(
                        "Go to strategy simulator",
                        id="strategy-link",
                        href="/Strategy",
                        style={"height": "4%"},
                    ),
                    dcc.Graph(
                        id="map_circuit",
                        config={"displayModeBar": False},
                        figure={},
                        style={"height": "50%", "width": "100%", "margin-top": "3%"},
                    ),
                    dcc.RadioItems(
                        id="map-style-radio",
                        options=[
                            {"label": "Streets", "value": "streets"},
                            {"label": "Satellite", "value": "satellite"},
                        ],
                        value="streets",
                        labelStyle={"display": "inline-block"},
                        style={"height": "5%"},
                        className="data-content",
                    ),
                ],
                style={"overflow": "auto", "height": "100%"},
            )
        ]

    @app.callback(
        Output("strategy-link", "href"),
        [Input("map", "clickData")],
    )
    def update_strategy_link(clickData):
        """Update the link for the strategy simulator with clickData"""
        if clickData is None:
            clickData = data4app.default_clickdata

        # temp
        totallap = clickData["points"][0]["customdata"]["totallap"]
        pitloss = clickData["points"][0]["customdata"]["pitloss"]
        medium_pace = clickData["points"][0]["customdata"]["medium_pace"]
        medium_degradation = clickData["points"][0]["customdata"]["medium_degradation"]
        if totallap is None:
            totallap = 999
        if pitloss is not None:
            pitloss = round(pitloss, 3)
        else:
            pitloss = 999
        if medium_pace is not None:
            medium_pace = round(medium_pace, 3)
        else:
            medium_pace = 999
        if medium_degradation is not None:
            medium_degradation = round(medium_degradation, 3)
        else:
            medium_degradation = 999
        values = {
            "totallap": totallap,
            "pitloss": pitloss,
            "medium_pace": medium_pace,
            "medium_degradation": medium_degradation,
        }

        params = urllib.parse.urlencode(values)
        new_url = f"/Strategy?{params}"
        return new_url


def register_page2_callbacks(app):
    """Register callbacks for the page2"""

    @app.callback(
        Output("simulation-results", "figure"),
        [Input("run-simulation-button", "n_clicks")],
        [
            State("Total-Laps", "value"),
            State("Pitloss", "value"),
            State("Soft-Pace", "value"),
            State("Medium-Pace", "value"),
            State("Hard-Pace", "value"),
            State("Soft-Degradation", "value"),
            State("Medium-Degradation", "value"),
            State("Hard-Degradation", "value"),
        ],
    )
    def update_output(
        n_clicks,
        totallap,
        pitloss,
        soft_pace,
        medium_pace,
        hard_pace,
        soft_degradation,
        medium_degradation,
        hard_degradation,
    ):
        if None in [
            totallap,
            pitloss,
            soft_pace,
            medium_pace,
            hard_pace,
            soft_degradation,
            medium_degradation,
            hard_degradation,
        ]:
            return "There is some missing values."
        dict_degradation = {
            "Soft": soft_degradation,
            "Medium": medium_degradation,
            "Hard": hard_degradation,
        }
        dict_pace = {"Soft": soft_pace, "Medium": medium_pace, "Hard": hard_pace}

        df_optimized = optimize_strategy(pitloss, totallap, dict_degradation, dict_pace)
        return create_strategy_figure(df_optimized)
