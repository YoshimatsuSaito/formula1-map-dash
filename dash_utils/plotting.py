import os
import sys

from plotly import graph_objects as go
from dotenv import load_dotenv


current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(os.path.dirname(current_dir), "modules"))

from geo import CircuitGeo


load_dotenv(".env")
MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")


def create_main_figure(df, latest_gp_index, latest_gp_legend):
    """Create the main figure."""
    fig = go.Figure()

    for idx, row in enumerate(df.itertuples()):
        if idx == latest_gp_index:
            color = "red"
            showlegend = True
            name = latest_gp_legend
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

    return fig


def create_circuit_figure(latest_gp_index, df, map_style, hoverData):
    """Create the circuit figure."""
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


def plot_circuit_location(fig, circuit_id, circuit_name, fp1, fp2, fp3, qualifying, sprint, race, gp_name, url, color, showlegend=False, name=None, **kwargs):
    """Plot a circuit location on a mapbox figure."""
    circuit_geo = CircuitGeo()

    lat_center, lon_center = circuit_geo.get_center(circuit_id)
    fig.add_trace(
        go.Scattermapbox(
            lat=[lat_center],
            lon=[lon_center],
            mode="markers",
            marker=dict(
                size=10,
                color=color,
                sizemode="diameter",
            ),
            customdata=[{
                "fp1":fp1, 
                "fp2":fp2,
                "fp3":fp3,
                "qualifying":qualifying, 
                "sprint":sprint,
                "race":race,
                "gp_name":gp_name,
                "url":url,
                "lat_center":lat_center,
                "lon_center":lon_center,
            }],
            hovertemplate=f"{circuit_name}<extra></extra>",
            name=name,
            showlegend=showlegend,
        ),
    )


def plot_circuit_shape(fig, circuit_id, circuit_name, fp1, fp2, fp3, qualifying, sprint, race, gp_name, url, color, **kwargs):
    """Plot a circuit shape on a mapbox figure."""
    circuit_geo = CircuitGeo()

    lat, lon = circuit_geo.get_lat_lon(circuit_id)
    lat_center, lon_center = circuit_geo.get_center(circuit_id)
    fig.add_trace(
        go.Scattermapbox(
            lat=lat,
            lon=lon,
            mode="lines",
            line=dict(width=2, color=color),
            customdata=[{
                "fp1":fp1, 
                "fp2":fp2,
                "fp3":fp3,
                "qualifying":qualifying, 
                "sprint":sprint,
                "race":race,
                "gp_name":gp_name,
                "url":url,
                "lat_center":lat_center,
                "lon_center":lon_center,
            }] * len(lat),
            hovertemplate=f"{circuit_name}<extra></extra>",
            showlegend=False,
        )
    )