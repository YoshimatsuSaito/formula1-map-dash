import os
import sys

import numpy as np
from plotly import graph_objects as go
from dotenv import load_dotenv


current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(os.path.dirname(current_dir), "modules"))

from geo import CircuitGeo


load_dotenv(".env")
MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
DICT_COMPOUND_COLOR = {"Soft": "red", "Medium": "yellow", "Hard": "white"}


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
        plot_circuit_location(
            fig=fig, color=color, showlegend=showlegend, name=name, **row._asdict()
        )
        plot_circuit_shape(fig=fig, color=color, **row._asdict())

    center_lat = df.loc[latest_gp_index, "lat"]
    center_lon = df.loc[latest_gp_index, "lon"]
    zoom = 1

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
            zoom=zoom,
        ),
        margin=dict(r=0, t=0, l=0, b=0),
        legend=dict(
            x=1,
            y=1,
            xanchor="right",
            yanchor="top",
            bgcolor="rgba(60, 60, 60, 0.5)",
            font=dict(color="black", family="Russo One"),
        ),
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
            showlegend = True
            name = "Circuit layout"
        else:
            color = "blue"
            showlegend = False
            name = None
        plot_circuit_location(
            fig=fig_circuit,
            color=color,
            showlegend=showlegend,
            name=name,
            **row._asdict(),
        )
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
            font=dict(color="black", family="Russo One"),
        ),
    )
    return fig_circuit


def create_strategy_figure(df_strategy, num_show=10):
    """Create possible strategies figure"""
    fig = go.Figure()
    dict_idx_total_lap_time = dict()

    for row in df_strategy.itertuples():
        list_compound = [
            x for x in [row.tyre_1, row.tyre_2, row.tyre_3, row.tyre_4] if x is not None
        ]
        list_lap = [
            x for x in [row.laps_1, row.laps_2, row.laps_3, row.laps_4] if x is not None
        ]
        list_color = [DICT_COMPOUND_COLOR[x] for x in list_compound]
        list_index = [(num_show - row.Index) * 2] * len(list_compound)
        dict_idx_total_lap_time[(num_show - row.Index) * 2] = convert_seconds_to_hms(
            row.total_lap_time
        )

        add_strategy(fig, list_lap, list_color, list_index)
        add_lap_annotation(fig, list_lap, list_index)

        add_strategy(fig, list_lap, list_color, list_index, add_space=True)

        if row.Index == num_show - 1:
            break

    add_color_legend(fig)

    fig.update_layout(
        barmode="stack",
        title="Top 10 Possible Race Strategies",
        plot_bgcolor="black",
        paper_bgcolor="black",
        font=dict(color="white"),
        yaxis=dict(
            showticklabels=True,
            tickvals=list(dict_idx_total_lap_time.keys()),
            ticktext=list(dict_idx_total_lap_time.values()),
        ),
        xaxis=dict(showticklabels=False, showgrid=False),
        legend=dict(orientation="h", yanchor="top", y=-0.1, xanchor="right", x=1),
    )

    return fig


def plot_circuit_location(
    fig,
    circuit_id,
    circuit_name,
    fp1,
    fp2,
    fp3,
    qualifying,
    sprint,
    race,
    gp_name,
    url,
    pitloss,
    totallap,
    medium_pace,
    medium_degradation,
    color,
    showlegend=False,
    name=None,
    **kwargs,
):
    """Add a circuit location on a mapbox plot."""
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
            customdata=[
                {
                    "fp1": fp1,
                    "fp2": fp2,
                    "fp3": fp3,
                    "qualifying": qualifying,
                    "sprint": sprint,
                    "race": race,
                    "gp_name": gp_name,
                    "url": url,
                    "lat_center": lat_center,
                    "lon_center": lon_center,
                    "circuit": circuit_name,
                    "pitloss": pitloss,
                    "totallap": totallap,
                    "medium_pace": medium_pace,
                    "medium_degradation": medium_degradation,
                }
            ],
            hovertemplate=f"{gp_name}<extra></extra>",
            name=name,
            showlegend=showlegend,
        ),
    )


def plot_circuit_shape(
    fig,
    circuit_id,
    circuit_name,
    fp1,
    fp2,
    fp3,
    qualifying,
    sprint,
    race,
    gp_name,
    url,
    pitloss,
    totallap,
    medium_pace,
    medium_degradation,
    color,
    showlegend=False,
    name=None,
    **kwargs,
):
    """Add a circuit shape on a mapbox plot."""
    circuit_geo = CircuitGeo()

    lat, lon = circuit_geo.get_lat_lon(circuit_id)
    lat_center, lon_center = circuit_geo.get_center(circuit_id)
    fig.add_trace(
        go.Scattermapbox(
            lat=lat,
            lon=lon,
            mode="lines",
            line=dict(width=2, color=color),
            customdata=[
                {
                    "fp1": fp1,
                    "fp2": fp2,
                    "fp3": fp3,
                    "qualifying": qualifying,
                    "sprint": sprint,
                    "race": race,
                    "gp_name": gp_name,
                    "url": url,
                    "lat_center": lat_center,
                    "lon_center": lon_center,
                    "circuit": circuit_name,
                    "pitloss": pitloss,
                    "totallap": totallap,
                    "medium_pace": medium_pace,
                    "medium_degradation": medium_degradation,
                }
            ]
            * len(lat),
            hovertemplate=f"{gp_name}<extra></extra>",
            name=name,
            showlegend=showlegend,
        )
    )


def add_lap_annotation(fig, list_lap, list_index):
    """Add number of lap annotation to a strategy graph"""
    cumsum_lap = np.cumsum(list_lap)
    for lap, idx in zip(cumsum_lap, list_index):
        fig.add_annotation(
            dict(
                x=lap,
                y=idx,
                text=str(lap),
                showarrow=False,
                font=dict(color="white", size=10),
                align="center",
                bordercolor="black",
                borderwidth=2,
                borderpad=4,
                bgcolor="black",
                opacity=0.8,
            )
        )


def add_strategy(fig, list_lap, list_color, list_index, add_space=False):
    """Add strategy bar graph to a strategy figure"""
    if add_space:
        list_index = [x - 1 for x in list_index]
        fig.add_trace(
            go.Bar(
                x=list_lap,
                y=list_index,
                base=np.cumsum([0] + list_lap[:-1]),
                orientation="h",
                name="",
                hoverinfo="none",
                hovertemplate=None,
                showlegend=False,
                hoverlabel=dict(namelength=0),
                marker_color=["rgba(0,0,0,0)"] * len(list_color),
                marker_line_width=0,
            )
        )
    else:
        fig.add_trace(
            go.Bar(
                x=list_lap,
                y=list_index,
                base=np.cumsum([0] + list_lap[:-1]),
                marker_color=list_color,
                orientation="h",
                name="",
                hoverinfo="none",
                hovertemplate=None,
                showlegend=False,
                hoverlabel=dict(namelength=0),
            )
        )


def add_color_legend(fig):
    """Add a tyre compound color mapping legend to a strategy figure"""
    for compound, color in DICT_COMPOUND_COLOR.items():
        fig.add_trace(
            go.Bar(
                x=[1],
                y=[compound],
                marker_color=color,
                orientation="h",
                name=compound,
                showlegend=True,
            )
        )


def convert_seconds_to_hms(seconds):
    """Convert seconds to string format"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    if m < 10:
        m = f"0{m}"
    if s < 10:
        s = f"0{s}"
    return f"{h}h {m}m {s}s"
