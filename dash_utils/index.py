import os
import sys

from dash import dcc, html
from dash.dependencies import Input, Output

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(os.path.dirname(current_dir), "dash_utils"))

from layout import get_page1_layout, get_page2_layout


def register_index_callback(app, fig, SEASON):
    @app.callback(Output("page-content", "children"),
                  Input("url", "pathname"))
    def display_page(pathname):
        if pathname == "/Strategy":
            return get_page2_layout()
        elif pathname == "/Prediction":
            return html.Div(children=[
                html.Div("Prediction"),
                dcc.Link("Back to Home", href="/")
            ])
        else:
            return get_page1_layout(fig, SEASON)
