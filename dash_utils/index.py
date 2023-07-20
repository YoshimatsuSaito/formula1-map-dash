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
        [Input("url", "pathname"),
        Input("strategy-data-store", "data")]
    )
    def display_page(pathname, data):
        """Display page by url passed"""
        if pathname == "/Strategy":
            # values = urllib.parse.parse_qs(urllib.parse.urlparse(search).query).get('values', [None])[0]
            # print(values)
            # if values is not None:
            #     values = json.loads(urllib.parse.unquote(values))
            if data is None:
                data = (60, 20, 90, 0.05)
            return get_page2_layout(*data)
        elif pathname == "/Prediction":
            return html.Div(children=[
                html.Div("Prediction"),
                dcc.Link("Back to Home", href="/")
            ])
        else:
            return get_page1_layout(fig, SEASON)
