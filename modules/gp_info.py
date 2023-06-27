import pytz
from ergast_py import Ergast

import pandas as pd

japan_timezone = pytz.timezone('Asia/Tokyo')


class SeasonInfo:
    """Get information about designated season"""
    def __init__(self, season):
        self.ergast = Ergast()
        self.season_info = self.ergast.season(season).get_races()
    
    def get_circuit_id(self):
        """Get circuit id of the season"""
        return [x.circuit.circuit_id for x in self.season_info]

    def get_circuit_name(self):
        """Get circuit name of the season"""
        return [x.circuit.circuit_name for x in self.season_info]

    def get_event_time(self, event="race", timezone=japan_timezone):
        """Get event datetime of the season"""
        if event == "race":
            return [x.date.astimezone(timezone).strftime("%m/%d %H:%M") for x in self.season_info]
        elif event == "fp1":
            return [x.first_practice.astimezone(timezone).strftime("%m/%d %H:%M") if x.first_practice is not None else None for x in self.season_info]
        elif event == "fp2":
            return [x.second_practice.astimezone(timezone).strftime("%m/%d %H:%M") if x.second_practice is not None else None for x in self.season_info]
        elif event == "fp3":
            return [x.third_practice.astimezone(timezone).strftime("%m/%d %H:%M") if x.third_practice is not None else None for x in self.season_info]
        elif event == "sprint":
            return [x.sprint.astimezone(timezone).strftime("%m/%d %H:%M") if x.sprint is not None else None for x in self.season_info]
        elif event == "qualifying":
            return [x.qualifying.astimezone(timezone).strftime("%m/%d %H:%M") for x in self.season_info]
        return None

    def get_gp_name(self):
        """Get grand prix name"""
        return [f"Round {x.round_no} {x.race_name}" for x in self.season_info]

    def get_url(self):
        """Get url of the season"""
        return [x.url for x in self.season_info]

    def get_df_all_info(self):
        """Get all information"""
        return pd.DataFrame({
            "circuit_id": self.get_circuit_id(),
            "circuit_name": self.get_circuit_name(),
            "fp1": self.get_event_time(event="fp1"),
            "fp2": self.get_event_time(event="fp2"),
            "fp3": self.get_event_time(event="fp3"),
            "qualifying": self.get_event_time(event="qualifying"),
            "sprint": self.get_event_time(event="sprint"),
            "race": self.get_event_time(event="race"),
            "gp_name": self.get_gp_name(),
            "url": self.get_url(),
        })
