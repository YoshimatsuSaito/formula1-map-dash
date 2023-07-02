import os
import sys

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dotenv import load_dotenv
from plotly import graph_objects as go

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(os.path.dirname(current_dir), "dash_utils"))

from plotting import plot_circuit_location, plot_circuit_shape

load_dotenv(".env")
MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")


def register_callbacks(app, df, latest_gp_index):
    """Register callbacks for the app."""

    @app.callback(
        Output("map_circuit", "figure"),
        [Input("map-style-radio", "value"),
        Input("map", "clickData")],
    )
    def update_circuit_figure(map_style, hoverData):
        lat_center = hoverData["points"][0]["customdata"]["lat_center"]
        lon_center = hoverData["points"][0]["customdata"]["lon_center"]

        fig_circuit = go.Figure()
        for idx, row in enumerate(df.itertuples()):
            if idx == latest_gp_index:
                color = "red"
            else:
                color = "blue"
            plot_circuit_location(fig=fig_circuit, color=color, **row._asdict())
            plot_circuit_shape(fig=fig_circuit, color=color, **row._asdict())

        fig_circuit.update_layout(
            autosize=True,
            mapbox=dict(
                accesstoken=MAPBOX_TOKEN,
                bearing=0,
                style=map_style,
                center=dict(lat=lat_center, lon=lon_center),
                pitch=0,
                zoom=12,
            ),
            margin=dict(l=2, t=0, b=0),
        )
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
