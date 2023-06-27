import os

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from plotly import graph_objects as go
from dotenv import load_dotenv

from modules.gp_info import SeasonInfo
from modules.plot_circuit import plot_circuit


load_dotenv(".env")
MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
SEASON = 2023

app = dash.Dash(__name__)
fig = go.Figure()
si = SeasonInfo(SEASON)
for circuit_id in si.get_circuit_id():
    plot_circuit(fig, circuit_id)

fig.update_layout(
    title="F1 Circuits",
    autosize=True,
    hovermode="closest",
    showlegend=False,
    mapbox=dict(
        accesstoken=MAPBOX_TOKEN,
        bearing=0,
        style="light",
        center=dict(lat=35, lon=136),
        pitch=0,
        zoom=1,
    ),
)


@app.callback(
    Output("hover-data", "children"),
    Input("map", "hoverData"),
)
def update_hover_data(hoverData):
    # print(hoverData["points"][0])
    if hoverData is not None:
        image = hoverData["points"][0]["customdata"]["image"]
        text = hoverData["points"][0]["customdata"]["text"]
        url = "https://www.formula1.com/en/racing/2023/Japan/Circuit.html"
        return html.Iframe(src=url, style={"width": "100%", "height": "100%"})
        # return [
        #     html.Img(src=image, style={"width": "100%", "height": "auto"}),
        #     html.P(text),
        # ]
    return []


app.layout = html.Div(
    style={"display": "flex"},
    children=[
        dcc.Graph(
            id="map",
            config={"displayModeBar": True},
            figure=fig,
            style={"height": "100vh", "flex": "70%"}
        ),
        html.Div(
            id="hover-data",
            style={"flex": "30%", "height": "100vh"}
        )
    ]
)


if __name__ == "__main__":
    app.run_server(debug=True)
