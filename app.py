import os

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from plotly import graph_objects as go
from dotenv import load_dotenv

from modules.gp_info import SeasonInfo
from modules.plot_circuit import plot_circuit_location, plot_circuit_shape

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
        name = f"Next: {si.get_gp_name()[latest_gp_index]}"
    else:
        color = "blue"
        showlegend = False
        name = "None"
    plot_circuit_location(fig=fig, color=color, showlegend=showlegend, name=name, **row._asdict())
    plot_circuit_shape(fig=fig, color=color, **row._asdict())

center_lat = df.loc[latest_gp_index, "lat"]
center_lon = df.loc[latest_gp_index, "lon"]

fig.update_layout(
    autosize=True,
    hovermode="closest",
    mapbox=dict(
        accesstoken=MAPBOX_TOKEN,
        bearing=0,
        style="streets",
        center=dict(lat=center_lat, lon=center_lon),
        pitch=0,
        zoom=1,
    ),
    margin=dict(r=5, t=5),
    legend=dict(
        x=0.5,
        y=-0.1,
        xanchor="center",
        yanchor="bottom",
    )
)


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


app.layout = html.Div(
    style={"display": "flex", "flex-direction": "column"},
    children=[
        html.Div(
            style={"height": "18vh"},
            children=[
                html.H1(f"FIA Formula One World Championship {SEASON}", style={"font-family": "Russo One", "padding": "0px", "margin-bottom": "0px", "margin-left": "5%"}),
                html.H5("Click a point and see information about the grand prix", style={"font-family": "Russo One", "padding": "0px", "margin-bottom": "0px",  "margin-top": "0px", "margin-left": "5%"})
            ]
        ),
        html.Div(
            style={"display": "flex", "flex-direction": "row", "height": "82vh"},
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
        ),
    ]
)


if __name__ == "__main__":
    app.run_server(debug=True)
