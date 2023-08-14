import json
import os
import sys

import urllib
from dash import dcc, html
from dash.dependencies import Input, Output

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(os.path.dirname(current_dir), "dash_utils"))

from layout import get_page1_layout, get_page2_layout


def register_index_callback(app, fig, SEASON):
    @app.callback(
        Output("page-content", "children"),
        [Input("url", "pathname"), Input("url", "search")],
    )
    def display_page(pathname, search):
        """Display page by url passed"""
        if pathname == "/Strategy":
            params = urllib.parse.parse_qs(search.lstrip("?"))
            totallap = int(params.get("totallap", [999])[0])
            pitloss = float(params.get("pitloss", [999])[0])
            medium_pace = float(params.get("medium_pace", [999])[0])
            medium_degradation = float(params.get("medium_degradation", [999])[0])
            data = (totallap, pitloss, medium_pace, medium_degradation)
            return get_page2_layout(*data)
        elif pathname == "/Prediction":
            params = urllib.parse.parse_qs(search.lstrip("?"))
            n_round = params.get("n_round")[0]
            return html.Div(
                children=[html.Div("Prediction"), dcc.Link(f"Back to Home {n_round}", href="/")]
            )
        else:
            return get_page1_layout(fig, SEASON)
