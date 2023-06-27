import os
import sys

from plotly import graph_objects as go

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(os.path.dirname(current_dir), "modules"))

from geo import CircuitGeo


def plot_circuit(fig, circuit_id, circuit_name, fp1, fp2, fp3, qualifying, sprint, race, gp_name, url, **kwargs):
    """Plot a circuit on a mapbox figure."""
    circuit_geo = CircuitGeo()

    lat_center, lon_center = circuit_geo.get_center(circuit_id)
    fig.add_trace(
        go.Scattermapbox(
            lat=[lat_center],
            lon=[lon_center],
            mode="markers",
            marker=dict(
                size=10,
                color="red",
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
                "url":url
            }],
            hovertemplate=f"{circuit_name}<extra></extra>"
        ),
    )
    
    lat, lon = circuit_geo.get_lat_lon(circuit_id)
    fig.add_trace(
        go.Scattermapbox(
            lat=lat,
            lon=lon,
            mode="lines",
            line=dict(width=2, color="red"),
            customdata=[{
                "fp1":fp1, 
                "fp2":fp2,
                "fp3":fp3,
                "qualifying":qualifying, 
                "sprint":sprint,
                "race":race,
                "gp_name":gp_name,
                "url":url
            }] * len(lat),
            hovertemplate=f"{circuit_name}<extra></extra>"
        )
    )
    
