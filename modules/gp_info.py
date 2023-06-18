import pytz
from ergast_py import Ergast

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

    def get_datetime(self, timezone=japan_timezone):
        """Get race datetime of the season"""
        return [x.date.astimezone(timezone) for x in self.season_info]
