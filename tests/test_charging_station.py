import sys
import os
from unittest import mock
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from chargingstation import ChargingStation

def test_charging_station_creation():
    station = ChargingStation("001", "10115", 52.5200, 13.4050)
    assert station.station_id == "001", "Station ID does not match"
    assert station.postal_code == "10115", "Postal code does not match"
    assert station.latitude == 52.5200, "Latitude does not match"
    assert station.longitude == 13.4050, "Longitude does not match"

def test_add_feedback():
    station = ChargingStation("001", "10115", 52.5200, 13.4050)
    station.addFeedback({"user": "user123", "feedback": "Great station!"})
    assert len(station.feedbacks) == 1, "Feedback was not added"
