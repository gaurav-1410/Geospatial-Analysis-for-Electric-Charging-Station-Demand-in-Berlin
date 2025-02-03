from typing import List, Optional
from charging_station import ChargingStation

class Area:
    def __init__(self, postal_code: str) -> None:
        """
        Initializes an Area object with a given postal code and an empty list of charging stations.

        :param postal_code: The postal code of the area.
        """
        self.postal_code: str = postal_code
        self.stations: List['ChargingStation'] = []

    def add_charging_station(self, chargingStation: 'ChargingStation') -> None:
        """
        Adds a charging station to the area if the station's postal code matches the area's postal code.

        :param chargingStation: The ChargingStation object to be added.
        """
        if chargingStation.postal_code == self.postal_code:
            self.stations.append(chargingStation)

    def find_station_by_id(self, station_id: str) -> Optional['ChargingStation']:
        """
        Searches for a charging station by its ID.

        :param station_id: The ID of the station to search for.
        :return: The ChargingStation object if found, otherwise None.
        """
        for station in self.stations:
            if station.station_id == station_id:
                return station
        return None