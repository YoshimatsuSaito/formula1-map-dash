from pathlib import Path

import json

current_dir = Path(__file__).resolve()

DICT_CIRCUIT_URL = {
    "abudhabi": "ae-2009.geojson",
    "spielberg":"at-1969.geojson",
    "melbourne": "au-1953.geojson",
    "baku": "az-2016.geojson",
    "spa": "be-1925.geojson",
    "sakhir": "bh-2002.geojson",
    "saopaulo": "br-1940.geojson",
    "montreal": "ca-1978.geojson",
    "shanghai": "cn-2004.geojson",
    "nurburg": "de-1927.geojson",
    "suzuka": "jp-1962.geojson",
}



class CircuitGeo:
    """Class to get geojson data of circuits from github"""
    def __init__(self):
        self.data_dir = current_dir.parent.parent / "data"

    def get_geojson(self, circuit):
        """Get geojson data of circuit"""
        with open(Path(self.data_dir, DICT_CIRCUIT_URL[circuit]), "r") as f:
            geo_data = json.load(f)
        return geo_data

    def get_lat_lon(self, circuit):
        """Get latitude and longitude of circuit"""
        geo_data = self.get_geojson(circuit)
        lat = [x[1] for x in geo_data['features'][0]['geometry']['coordinates']]
        lon = [x[0] for x in geo_data['features'][0]['geometry']['coordinates']]
        return lat, lon

    def get_bbox(self, circuit):
        """Get bounding box of circuit"""
        geo_data = self.get_geojson(circuit)
        min_lon, min_lat, max_lon, max_lat = geo_data['features'][0]['bbox']
        lon_extend = (max_lon - min_lon) /2
        lat_extend = (max_lat - min_lat) /2
        min_lon -= lon_extend
        max_lon += lon_extend
        min_lat -= lat_extend
        max_lat += lat_extend
        lon = [min_lon, min_lon, max_lon, max_lon, min_lon]
        lat = [min_lat, max_lat, max_lat, min_lat, min_lat]
        return lat, lon

    def get_center(self, circuit):
        """Get bounding box of circuit"""
        geo_data = self.get_geojson(circuit)
        min_lon, min_lat, max_lon, max_lat = geo_data['features'][0]['bbox']
        lon = (max_lon + min_lon) /2
        lat = (max_lat + min_lat) /2
        return lat, lon
    