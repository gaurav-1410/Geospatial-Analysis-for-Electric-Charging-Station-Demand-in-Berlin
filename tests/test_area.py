import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from area import Area
from chargingstation import ChargingStation

def test_area_creation():
    area = Area("10115")
    assert area.postal_code == "10115", "Postal code does not match"
    assert len(area.stations) == 0, "Stations list should be empty initially"

def test_add_charging_station():
    area = Area("10115")
    station = ChargingStation("001", "10115", 52.5200, 13.4050)
    area.addChargingStation(station)
    assert len(area.stations) == 1, "Station was not added"
    assert area.stations[0].station_id == "001", "Station ID does not match"

def test_find_station_by_id():
    area = Area("10115")
    station = ChargingStation("001", "10115", 52.5200, 13.4050)
    area.addChargingStation(station)
    result = area.find_station_by_id("001")
    assert result == station, "Station ID not found correctly"
