import os
import sys
from math import log

from plotly import graph_objects as go
from dotenv import load_dotenv


current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(os.path.dirname(current_dir), "modules"))

from geo import CircuitGeo


load_dotenv(".env")
MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")


# def calc_zoom(lat, lon):
#     """Calculate the zoom level for a mapbox figure."""
#     max_bound = (
#         max(
#             abs(lat.max() - lat.min()),
#             abs(lon.max() - lon.min()),
#         )
#         * 111
#     )
#     zoom = 13.5 - log(max_bound)
#     return zoom


def create_main_figure(df, latest_gp_index, latest_gp_legend):
    """Create the main figure."""
    fig = go.Figure()

    cnt = 0
    for idx, row in enumerate(df.itertuples()):
        if idx == latest_gp_index:
            color = "red"
            showlegend = True
            name = f"Next: {latest_gp_legend}"
        elif cnt == 0:
            color = "blue"
            showlegend = True
            name = "Grand Prix"
            cnt = -1
        else:
            color = "blue"
            showlegend = False
            name = None
        plot_circuit_location(fig=fig, color=color, showlegend=showlegend, name=name, **row._asdict())
        plot_circuit_shape(fig=fig, color=color, **row._asdict())

    center_lat = df.loc[latest_gp_index, "lat"]
    center_lon = df.loc[latest_gp_index, "lon"]

    fig.update_layout(
        title="Grand prix map",
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
        margin=dict(r=0, t=0, l=0, b=0),
        legend=dict(
            x=1,
            y=1,
            xanchor="right",
            yanchor="top",
            bgcolor="rgba(60, 60, 60, 0.5)",
            font=dict(color="black", family="Russo One")
        )
    )

    return fig


def create_circuit_figure(latest_gp_index, df, map_style, clickData):
    """Create the circuit figure."""
    lat_center = clickData["points"][0]["customdata"]["lat_center"]
    lon_center = clickData["points"][0]["customdata"]["lon_center"]

    fig_circuit = go.Figure()
    for idx, row in enumerate(df.itertuples()):
        if idx == latest_gp_index:
            color = "red"
            showlegend=True
            name=f"{row.circuit_name}"
        else:
            color = "blue"
            showlegend=False
            name=None
        plot_circuit_location(fig=fig_circuit, color=color, showlegend=showlegend, name=name, **row._asdict())
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
        margin=dict(l=0, t=0, b=0, r=0),
        legend=dict(
            x=1,
            y=1,
            xanchor="right",
            yanchor="top",
            bgcolor="rgba(60, 60, 60, 0.5)",
            font=dict(color="black", family="Russo One")
        )
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
                "circuit": circuit_name,
            }],
            hovertemplate=f"{gp_name}<extra></extra>",
            name=name,
            showlegend=showlegend,
        ),
    )


def plot_circuit_shape(fig, circuit_id, circuit_name, fp1, fp2, fp3, qualifying, sprint, race, gp_name, url, color, showlegend=False, name=None, **kwargs):
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
                "circuit": circuit_name,
            }] * len(lat),
            hovertemplate=f"{gp_name}<extra></extra>",
            name=name,
            showlegend=showlegend,
        )
    )