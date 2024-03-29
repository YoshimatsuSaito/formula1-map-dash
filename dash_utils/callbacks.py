import os
import sys
import urllib

import pytz
from dash import dcc, html
from dash.dependencies import Input, Output, State
from plotly import graph_objects as go

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(os.path.dirname(current_dir), "dash_utils"))
sys.path.append(os.path.join(os.path.dirname(current_dir), "modules"))

from plotting import create_circuit_figure, create_strategy_figure
from strategy_maker import optimize_strategy

jst = pytz.timezone("Asia/Tokyo")


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
        gp_round_name = clickData["points"][0]["customdata"]["gp_round_name"]
        url = clickData["points"][0]["customdata"]["url"]
        circuit = clickData["points"][0]["customdata"]["circuit"]
        return [
            html.Div(
                [
                    html.Div(
                        f"{gp_round_name}",
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
                        id="prediction-link",
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
                        style={"height": "50%", "width": "100%", "margin-top": "2%"},
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

    @app.callback(
        Output("prediction-link", "href"),
        [Input("map", "clickData")],
    )
    def update_prediction_link(clickData):
        """Update the link for the strategy simulator with clickData"""
        if clickData is None:
            clickData = data4app.default_clickdata

        n_round = clickData["points"][0]["customdata"]["n_round"]
        gp_round_name = clickData["points"][0]["customdata"]["gp_round_name"]
        wiki_url = clickData["points"][0]["customdata"]["url"]
        race = clickData["points"][0]["customdata"]["race"]

        current_time_jst = datetime.now(jst)
        specified_time_jst = datetime.strptime(
            f"{current_time_jst.year}/{race}", "%Y/%m/%d %H:%M"
        )
        specified_time_jst = jst.localize(specified_time_jst)
        if current_time_jst > specified_time_jst:
            is_past = 1
        else:
            is_past = 0

        values = {
            "n_round": n_round,
            "gp_round_name": gp_round_name,
            "wiki_url": wiki_url,
            "is_past": is_past,
        }
        params = urllib.parse.urlencode(values)
        new_url = f"/Prediction?{params}"
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
            fig = go.Figure()
            fig.update_layout(
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                annotations=[
                    dict(
                        text="Enter the necessary<br>parameters above.",
                        xref="paper",
                        yref="paper",
                        showarrow=False,
                        font=dict(size=20),
                    )
                ],
                margin=dict(r=0, t=0, l=0, b=0),
                autosize=True,
            )
            return fig
        dict_degradation = {
            "Soft": soft_degradation,
            "Medium": medium_degradation,
            "Hard": hard_degradation,
        }
        dict_pace = {"Soft": soft_pace, "Medium": medium_pace, "Hard": hard_pace}

        df_optimized = optimize_strategy(pitloss, totallap, dict_degradation, dict_pace)
        return create_strategy_figure(df_optimized)

    @app.callback(
        Output("explanation-area-strategy", "style"),
        Output("toggle-button-strategy", "children"),
        [Input("toggle-button-strategy", "n_clicks")],
    )
    def toggle_collapse(n_clicks):
        if n_clicks % 2 == 0:
            return {"display": "none"}, "Show User Guide"
        else:
            return {
                "display": "block",
                "background-color": "#f2f2f2",
                "border": "2px solid black",
                "margin": "20px",
                "padding": "20px",
                "overflow": "auto",
            }, "Hide User Guide"
