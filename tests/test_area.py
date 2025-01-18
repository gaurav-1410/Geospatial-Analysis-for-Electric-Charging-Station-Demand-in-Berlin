import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from src.area import Area
from src.charging_station import ChargingStation
from typing import Optional

def test_area_creation() -> None:
    """
    Test the creation of an Area instance.
    :return: None
    """
    area = Area("10115")
    assert area.postal_code == "10115", "Postal code does not match"
    assert len(area.stations) == 0, "Stations list should be empty initially"

def test_add_charging_station() -> None:
    """
    Test adding a ChargingStation to an Area.
    :return: None
    """
    area = Area("10115")
    station = ChargingStation("001", "10115", 52.5200, 13.4050)
    area.add_charging_station(station)
    assert len(area.stations) == 1, "Station was not added"
    assert area.stations[0].station_id == "001", "Station ID does not match"

def test_find_station_by_id() -> None:
    """
    Test finding a ChargingStation by its ID in an Area.
    :return: None
    """
    area = Area("10115")
    station = ChargingStation("001", "10115", 52.5200, 13.4050)
    area.add_charging_station(station)
    result = area.find_station_by_id("001")
    assert result == station, "Station ID not found correctly"

def test_find_station_by_id_not_found() -> None:
    """
    Test finding a ChargingStation by ID when the station does not exist.
    :return: None
    """
    area = Area("10115")
    # Finding a station that doesn't exist
    result: Optional[ChargingStation] = area.find_station_by_id("999")
    assert result is None, "The result should be None when the station is not found"
