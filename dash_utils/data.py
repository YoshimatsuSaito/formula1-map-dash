from dataclasses import dataclass

import pandas as pd

from modules.gp_info import SeasonInfo

SEASON = 2023


@dataclass
class Data4App:
    """Data for the app."""
    si: SeasonInfo
    latest_gp_index: int
    latest_gp_legend: str
    df: pd.DataFrame


def create_data():
    """Create data for the app."""
    si = SeasonInfo(SEASON)
    latest_gp_index = si.get_latest_gp_index()
    latest_gp_legend = si.get_gp_name()[latest_gp_index]
    df = si.get_df_all_info()
    return Data4App(si, latest_gp_index, latest_gp_legend, df)
