import os
import sys

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(os.path.dirname(current_dir), "dash_utils"))

from plotting import create_circuit_figure


def register_callbacks(app, df, latest_gp_index):
    """Register callbacks for the app."""

    @app.callback(
        Output("map_circuit", "figure"),
        [Input("map-style-radio", "value"),
        Input("map", "clickData")],
    )
    def update_circuit_figure(map_style, hoverData):
        """Update the circuit figure."""
        fig_circuit = create_circuit_figure(latest_gp_index, df, map_style, hoverData)
        return fig_circuit


    @app.callback(
        Output("hover-data", "children"),
        Input("map", "clickData"),
    )
    def update_hover_data(hoverData):
        if hoverData is not None:
            fp1 = hoverData["points"][0]["customdata"]["fp1"]
            fp2 = hoverData["points"][0]["customdata"]["fp2"]
            fp3 = hoverData["points"][0]["customdata"]["fp3"]
            qualifying = hoverData["points"][0]["customdata"]["qualifying"]
            sprint = hoverData["points"][0]["customdata"]["sprint"]
            race = hoverData["points"][0]["customdata"]["race"]
            gp_name = hoverData["points"][0]["customdata"]["gp_name"]
            url = hoverData["points"][0]["customdata"]["url"]
            return [
                html.Div([
                    html.Div(f"{gp_name}", style={"font-family": "Russo One", "padding": "5px"}),
                    html.Div(f"FP1: {fp1}", style={"font-family": "Russo One", "padding": "5px"}),
                    html.Div(f"FP2: {fp2}", style={"font-family": "Russo One", "padding": "5px"}),
                    html.Div(f"FP3: {fp3}", style={"font-family": "Russo One", "padding": "5px"}),
                    html.Div(f"Qualifying: {qualifying}", style={"font-family": "Russo One", "padding": "5px"}),
                    html.Div(f"Sprint: {sprint}", style={"font-family": "Russo One", "padding": "5px"}),
                    html.Div(f"Race: {race}", style={"font-family": "Russo One", "padding": "5px"}),
                    dcc.Graph(
                            id="map_circuit",
                            config={"displayModeBar": False},
                            figure={},
                            style={"height": "40%", "width": "100%"},
                        ),
                    dcc.RadioItems(
                        id='map-style-radio',
                        options=[
                            {'label': 'Streets', 'value': 'streets'},
                            {'label': 'Satellite', 'value': 'satellite'},
                        ],
                        value='streets',
                        labelStyle={"display": "inline-block"}
                    )
                ], style={"overflow": "auto", "height": "100%", "padding-top": "0%"})
            ]
        return []
