import os

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from plotly import graph_objects as go
from dotenv import load_dotenv

from modules.gp_info import SeasonInfo
from modules.plot_circuit import plot_circuit

external_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap"
]
load_dotenv(".env")
MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
SEASON = 2023

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
fig = go.Figure()
si = SeasonInfo(SEASON)
latest_gp_index = si.get_latest_gp_index()
df = si.get_df_all_info()
for idx, row in enumerate(df.itertuples()):
    if idx == latest_gp_index:
        color = "red"
        showlegend = True
        name = "Next Grand Prix"
    else:
        color = "blue"
        showlegend = False
        name = "None"
    plot_circuit(fig=fig, color=color, showlegend=showlegend, name=name, **row._asdict())

center_lat = df.loc[latest_gp_index, "lat"]
center_lon = df.loc[latest_gp_index, "lon"]

fig.update_layout(
    autosize=True,
    hovermode="closest",
    mapbox=dict(
        accesstoken=MAPBOX_TOKEN,
        bearing=0,
        style="light",
        center=dict(lat=center_lat, lon=center_lon),
        pitch=0,
        zoom=1,
    ),
    margin=dict(r=20, t=20),
    legend=dict(
        x=0.5,
        y=-0.1,
        xanchor="center",
        yanchor="bottom",
    )
)

@app.callback(
    Output("hover-data", "children"),
    Input("map", "hoverData"),
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
            ], style={"overflow": "auto", "height": "80%", "padding-top": "5%"})
        ]
    return []


app.layout = html.Div(
    style={"display": "flex", "flex-direction": "column"},
    children=[
        html.Div(
            style={"height": "10vh"},
            children=[
                html.H1(f"FIA Formula One World Championship {SEASON}", style={"font-family": "Russo One", "padding": "0px", "margin-bottom": "0px", "margin-left": "5%"})
            ]
        ),
        html.Div(
            style={"display": "flex", "flex-direction": "row", "height": "90vh"},
            children=[
                dcc.Graph(
                    id="map",
                    config={"displayModeBar": False},
                    figure=fig,
                    style={"height": "100%", "flex": "60%"}
                ),
                html.Div(
                    id="hover-data",
                    style={"flex": "40%", "height": "100%"}
                )
            ]
        ),
        html.Div(
            id="new-div",
            children=[
                html.Iframe(src="https://en.wikipedia.org/wiki/2023_Austrian_Grand_Prix", style={"height": "100vh", "width": "100vw"}),
            ],
            style={"height": "100vh", "width": "100vw"}
        )
    ]
)


if __name__ == "__main__":
    app.run_server(debug=True)
