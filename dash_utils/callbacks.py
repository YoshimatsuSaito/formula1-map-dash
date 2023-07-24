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

from plotting import create_circuit_figure, create_main_figure


def register_page1_callbacks(app, data4app):
    """Register callbacks for the app."""

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
            raise PreventUpdate

        # temp
        totallap = clickData["points"][0]["customdata"]["totallap"]
        pitloss = clickData["points"][0]["customdata"]["pitloss"]
        medium_pace = clickData["points"][0]["customdata"]["medium_pace"]
        medium_degradation = clickData["points"][0]["customdata"]["medium_degradation"]
        values = {
            "totallap": totallap,
            "pitloss": pitloss,
            "medium_pace": medium_pace,
            "medium_degradation": medium_degradation,
        }

        params = urllib.parse.urlencode(values)
        new_url = f"/Strategy?{params}"
        print(new_url)
        return new_url


# def register_page2_callbacks(app):
#     @app.callback(Output("strategy-data-store", "data"), [Input("map", "clickData")])
#     def update_strategy_data(clickData):
#         """Update url for strategy simulator"""
#         if clickData is None:
#             pass
#         total_laps = 50
#         pitloss = 20
#         soft_pace = 90
#         medium_degradation = 0.05
#         values = (total_laps, pitloss, soft_pace, medium_degradation)
#         return values
