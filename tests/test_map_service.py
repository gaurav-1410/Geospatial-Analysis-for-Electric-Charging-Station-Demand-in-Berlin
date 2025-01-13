import pandas as pd
import pytest
import sys
import os
from shapely.geometry import Point
import geopandas as gpd
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from src.map_service import MapService
from src.charging_station import ChargingStation

def test_create_map():
    # Create a GeoDataFrame with geometries and set a CRS
    gdf = gpd.GeoDataFrame({
        "PLZ": [10115],
        "Einwohner": [1000],
        "ChargingStations": [5],
        "geometry": [Point(13.388860, 52.517037)]  # Example coordinates (Berlin)
    }, crs="EPSG:4326")  # Assign WGS84 CRS (latitude/longitude)

    try:
        # Call the create_map method
        map_ = MapService.create_map("Residents", gdf, 5)
        assert map_ is not None, "Map creation failed"
    except Exception as e:
        pytest.fail(f"create_map raised an exception: {e}")

def test_find_nearby_stations():
    data = pd.DataFrame({
        "Latitude": [52.5200, 52.5250],
        "Longitude": [13.4050, 13.4100]
    })
    nearby_stations = MapService.find_nearby_stations(data, 52.5200, 13.4050, 2)
    assert len(nearby_stations) > 0, "No stations found within the radius"

def test_organize_stations_by_area():
    data = pd.DataFrame({
        "plz": [10115, 10115],
        "Latitude": [52.5200, 52.5250],
        "Longitude": [13.4050, 13.4100]
    })
    areas = MapService.organize_stations_by_area(data)
    assert 10115 in areas, "Area organization failed"
    assert len(areas[10115].stations) == 2, "Station count mismatch"
