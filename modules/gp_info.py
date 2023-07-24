import os
import pytz
import sys
import logging
from datetime import datetime
from ergast_py import Ergast

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from tqdm import tqdm

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(os.path.dirname(current_dir), "modules"))

from geo import CircuitGeo
from wiki import DICT_CIRCUIT_GPNAME, WikiSearcher

my_logger = logging.getLogger("my_logger")
my_logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
my_logger.addHandler(handler)

japan_timezone = pytz.timezone("Asia/Tokyo")


class SeasonInfo:
    """Get information about designated season"""

    def __init__(self, season):
        self.season_info = Ergast().season(season).get_races()
        self.season = season

    def get_circuit_id(self):
        """Get circuit id of the season"""
        return [x.circuit.circuit_id for x in self.season_info]

    def get_circuit_name(self):
        """Get circuit name of the season"""
        return [x.circuit.circuit_name for x in self.season_info]

    def get_event_time(self, event="race", timezone=japan_timezone):
        """Get event datetime of the season"""
        if event == "race":
            return [
                x.date.astimezone(timezone).strftime("%m/%d %H:%M")
                for x in self.season_info
            ]
        elif event == "fp1":
            return [
                x.first_practice.astimezone(timezone).strftime("%m/%d %H:%M")
                if x.first_practice is not None
                else None
                for x in self.season_info
            ]
        elif event == "fp2":
            return [
                x.second_practice.astimezone(timezone).strftime("%m/%d %H:%M")
                if x.second_practice is not None
                else None
                for x in self.season_info
            ]
        elif event == "fp3":
            return [
                x.third_practice.astimezone(timezone).strftime("%m/%d %H:%M")
                if x.third_practice is not None
                else None
                for x in self.season_info
            ]
        elif event == "sprint":
            return [
                x.sprint.astimezone(timezone).strftime("%m/%d %H:%M")
                if x.sprint is not None
                else None
                for x in self.season_info
            ]
        elif event == "qualifying":
            return [
                x.qualifying.astimezone(timezone).strftime("%m/%d %H:%M")
                for x in self.season_info
            ]
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

    def get_recent_dry_race(self, list_circuit_id):
        """Get recent dry race"""
        list_gpname = [DICT_CIRCUIT_GPNAME[x] for x in list_circuit_id]
        # Get year to calculate pitloss (recent dry race)
        ws = WikiSearcher()
        list_year = [ws.get_recent_dry_race(x) for x in tqdm(list_gpname)]
        return list_year

    def get_data_for_strategy_simulator(self):
        """Get data for strategy simulator for each grand prix"""
        # Circuit that you want to get pitloss
        list_circuit_id = self.get_circuit_id()
        my_logger.info("Start get_recent_dry_race")
        list_recent_dry_year = self.get_recent_dry_race(list_circuit_id)
        # Get data with ergast api
        list_pitloss = []
        list_totallap = []
        list_medium_pace = []
        list_medium_degradation = []
        # Loop year whose condition was dry
        my_logger.info("Start loop for each recent dry year")
        for circuit_id, recent_dry_year in zip(list_circuit_id, list_recent_dry_year):
            my_logger.info(f"Process {circuit_id}: {recent_dry_year}")
            if recent_dry_year is None:
                pitloss = None
                totallap = None
                medium_pace = None
                medium_degradation = None
            else:
                # Get all races, circuit, and round of the year
                list_race_of_the_year = Ergast().season(recent_dry_year).get_races()
                dict_circuit_id_round_no = dict()
                for race_of_the_year in list_race_of_the_year:
                    _circuit_id = race_of_the_year.circuit.circuit_id
                    _round_no = race_of_the_year.round_no
                    if _circuit_id not in dict_circuit_id_round_no.keys():
                        dict_circuit_id_round_no[_circuit_id] = _round_no
                # Get target round
                target_round = dict_circuit_id_round_no[circuit_id]
                # Get winner
                target_driver = (
                    Ergast()
                    .season(recent_dry_year)
                    .round(target_round)
                    .result(1)
                    .get_driver()
                    .driver_id
                )

                # Get lap time of target driver
                list_lap_time = self.get_list_lap_time(
                    recent_dry_year, target_round, target_driver
                )
                list_pit_lap = self.get_pit_lap(
                    recent_dry_year, target_round, target_driver
                )

                # Get each data
                if list_pit_lap is not None:
                    pitloss = self.get_pit_loss(list_lap_time, list_pit_lap)
                    medium_degradation = self.get_degradation(
                        list_lap_time, list_pit_lap
                    )
                else:
                    pitloss = None
                    medium_degradation = None
                totallap = len(list_lap_time)
                medium_pace = np.median(list_lap_time)

            my_logger.info(
                f"Result: pitloss - {pitloss}, totallap - {totallap}, medium_pace - {medium_pace}, medium_degradation - {medium_degradation}"
            )
            list_pitloss.append(pitloss)
            list_totallap.append(totallap)
            list_medium_pace.append(medium_pace)
            list_medium_degradation.append(medium_degradation)

        return pd.DataFrame(
            {
                "circuit_id": list_circuit_id,
                "pitloss": list_pitloss,
                "totallap": list_totallap,
                "medium_pace": list_medium_pace,
                "medium_degradation": list_medium_degradation,
            }
        )

    def get_pit_lap(self, year, target_round, target_driver):
        """Get pit lap"""
        try:
            list_pit_stop = (
                Ergast()
                .season(year)
                .round(target_round)
                .driver(target_driver)
                .get_pit_stop()
                .pit_stops
            )
            list_pit_lap = [x.lap for x in list_pit_stop]
        # ergast_py does not work when too long pit stop occurs like red flag
        except ValueError:
            list_pit_lap = None
        return list_pit_lap

    def get_pit_loss(self, list_lap_time, list_pit_lap):
        """Get pitloss of given circuit and year"""
        # You have to get times of inlap and outlap
        list_2laps_when_pit = [sum(list_lap_time[x - 1 : x + 1]) for x in list_pit_lap]
        min_2laps_when_pit = min(list_2laps_when_pit)
        # Get median lap time
        med_lap = np.median(list_lap_time)
        # Calculate pit"loss" not pit duration
        pitloss = min_2laps_when_pit - med_lap * 2
        # For irregular case like VSC → SC etc..
        if pitloss > 30:
            return None
        return pitloss

    def get_degradation(self, list_lap_time, list_pit_lap):
        """Calculate degradation roughly"""
        # Add last lap -1 for last stint
        list_pit_lap.append(len(list_lap_time))
        list_degradation = []
        lap_start = 0
        # Loop for each stint
        for pit_lap in list_pit_lap:
            # Remove lap time of pit lap
            stint = np.array(list_lap_time[lap_start : pit_lap - 1])
            # Remove abnormaly slow laps
            stint = stint[stint < min(list_lap_time) * 1.08]
            x = np.arange(len(stint)).reshape(-1, 1)
            # Calc slope (=degradation)
            model = LinearRegression()
            try:
                model.fit(x, stint)
                list_degradation.append(model.coef_[0])
            except:
                pass
            # Update lap_start
            lap_start = pit_lap + 1
        # Calc degradation
        if len(list_degradation) > 0:
            return np.array(list_degradation).mean()
        return None

    def get_list_lap_time(self, year, target_round, driver):
        """Get lap times of a driver of year and round"""
        list_lap_time = []
        # Get lap times of winner (loop is for api limitation)
        for lap in tqdm(range(1, 101)):
            try:
                lap_time = (
                    Ergast()
                    .season(year)
                    .round(target_round)
                    .driver(driver)
                    .lap(lap)
                    .get_lap()
                    .laps[0]
                    .timings[0]
                    .time
                )
                lap_time = cvt_datetime_to_sec(lap_time)
                list_lap_time.append(lap_time)
            except:
                break
        return list_lap_time

    def get_df_all_info(self, read_data_for_strategy_simulator=True):
        """Get all information"""
        df = pd.DataFrame(
            {
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
            }
        )
        if read_data_for_strategy_simulator:
            # Read data that made in advance because it takes too much time to make data
            df_data_for_strategy_simulator = pd.read_csv(
                os.path.join(current_dir, "../data/data_for_strategy_maker.csv"),
            )
            df_data_for_strategy_simulator["totallap"] = df_data_for_strategy_simulator["totallap"].astype("Int64")
            df = pd.merge(df, df_data_for_strategy_simulator, on="circuit_id", how="left")
        else:
            for colname in ["pitloss", "totallap", "medium_pace", "medium_degradation"]:
                df[colname] = None
        return df


def cvt_datetime_to_sec(datetime_value):
    """Convert datetime to sec"""
    return (
        datetime_value.hour * 3600
        + datetime_value.minute * 60
        + datetime_value.second
        + datetime_value.microsecond / 1000000
    )
