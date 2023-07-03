import os
import pytz
import sys
from datetime import datetime
from ergast_py import Ergast

import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(os.path.dirname(current_dir), "modules"))

# TODO: use this
from geo import CircuitGeo

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

    def get_latitude(self):
        """Get latitude of each grand prix"""
        return [x.circuit.location.latitude for x in self.season_info]

    def get_longtiude(self):
        """Get longitude of each grand prix"""
        return [x.circuit.location.longitude for x in self.season_info]

    def get_latest_gp_index(self, timezone=japan_timezone):
        """Get index of latest grand prix"""
        today = datetime.now(timezone)
        list_date = [x.date.astimezone(timezone) for x in self.season_info]
        latest_gp_date = min(x for x in list_date if x >= today)
        return list_date.index(latest_gp_date)

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
            "lat": self.get_latitude(),
            "lon": self.get_longtiude(),
        })
