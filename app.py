import os

import dash
import dash_core_components as dcc
import dash_html_components as html
from plotly import graph_objects as go
from dotenv import load_dotenv

from modules.plot_circuit import plot_circuit
from modules.geo import DICT_CIRCUIT_URL

load_dotenv(".env")
MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")


app = dash.Dash(__name__)
fig = go.Figure()
for circuit in DICT_CIRCUIT_URL.keys():
    plot_circuit(fig, circuit)

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

app.layout = html.Div([
    dcc.Graph(
        id="map",
        config={"displayModeBar": True},
        figure=fig,
        style={"height": "100vh", "width": "100vw"}
    )
])


if __name__ == '__main__':
    app.run_server(debug=True)
