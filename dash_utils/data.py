from dataclasses import dataclass, field

import pandas as pd

from modules.gp_info import SeasonInfo


@dataclass
class Data4App:
    """Data for the app."""

    si: SeasonInfo
    latest_gp_index: int
    latest_gp_legend: str
    df: pd.DataFrame
    default_clickdata: dict = field(init=False)

    def __post_init__(self):
        self.default_clickdata = create_default_clickdata(self.df, self.latest_gp_index)


def create_data(SEASON):
    """Create data for the app."""
    si = SeasonInfo(SEASON)
    latest_gp_index = si.get_latest_gp_index()
    latest_gp_legend = si.get_gp_name()[latest_gp_index]
    df = si.get_df_all_info()
    return Data4App(si, latest_gp_index, latest_gp_legend, df)


def create_default_clickdata(df: pd.DataFrame, latest_gp_index: int):
    """Create default clickdata for the app."""
    return {
        "points": [
            {
                "customdata": {
                    "fp1": df.iloc[latest_gp_index]["fp1"],
                    "fp2": df.iloc[latest_gp_index]["fp2"],
                    "fp3": df.iloc[latest_gp_index]["fp3"],
                    "qualifying": df.iloc[latest_gp_index]["qualifying"],
                    "sprint": df.iloc[latest_gp_index]["sprint"],
                    "race": df.iloc[latest_gp_index]["race"],
                    "gp_name": df.iloc[latest_gp_index]["gp_name"],
                    "circuit": df.iloc[latest_gp_index]["circuit_name"],
                    "url": df.iloc[latest_gp_index]["url"],
                    "lat_center": df.iloc[latest_gp_index]["lat"],
                    "lon_center": df.iloc[latest_gp_index]["lon"],
                    "pitloss": df.iloc[latest_gp_index]["pitloss"],
                    "totallap": df.iloc[latest_gp_index]["totallap"],
                    "medium_pace": df.iloc[latest_gp_index]["medium_pace"],
                    "medium_degradation": df.iloc[latest_gp_index]["medium_degradation"],
                }
            }
        ]
    }
