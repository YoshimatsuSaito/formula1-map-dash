import os
import sys

from plotly import graph_objects as go

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(os.path.dirname(current_dir), "modules"))

from geo import CircuitGeo


def plot_circuit(fig, circuit):
    """Plot a circuit on a mapbox figure."""
    circuit_geo = CircuitGeo()

    lat_center, lon_center = circuit_geo.get_center(circuit)
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
            customdata=[{"image": f"/assets/{circuit}.jpg", "text": f"{circuit}"}],
            hovertemplate=f"{circuit}<extra></extra>"
        ),
    )
    
    lat, lon = circuit_geo.get_lat_lon(circuit)
    fig.add_trace(
        go.Scattermapbox(
            lat=lat,
            lon=lon,
            mode="lines",
            line=dict(width=2, color="red"),
            customdata=[{"image": f"/assets/{circuit}.jpg", "text": f"{circuit}"}] * len(lat),
            hovertemplate=f"{circuit}<extra></extra>"
        )
    )
    
