import os
import sys
import urllib

from dash.dependencies import Input, Output

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(os.path.dirname(current_dir), "dash_utils"))
sys.path.append(os.path.join(os.path.dirname(current_dir), "modules"))

from layout import get_page1_layout, get_page2_layout, get_page3_layout


def register_index_callback(app, fig, SEASON, df_prediction):
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
            return get_page2_layout(*data), None
        elif pathname == "/Prediction":
            params = urllib.parse.parse_qs(search.lstrip("?"))
            n_round = int(params.get("n_round")[0])
            gp_round_name = params.get("gp_round_name")[0]
            wiki_url = params.get("wiki_url")[0]
            is_past = int(params.get("is_past")[0])
            df_target = (
                df_prediction.loc[df_prediction["round"] == n_round]
                .sort_values(by="pred")
                .reset_index(drop=True)
            )
            df_target["target"] = (df_target["pred"] / df_target["pred"].sum()) * 100

            return get_page3_layout(gp_round_name, df_target, wiki_url, is_past)
        else:
            return get_page1_layout(fig, SEASON)
