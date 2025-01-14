import pytest
import sys
import os
import pandas as pd
from unittest import mock
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from src.data_service import DataService

def test_load_data_real():
    data_service = DataService()

    try:
        data, geo_data = data_service.load_data()
        assert isinstance(data, pd.DataFrame), "Data should be a pandas DataFrame"
        assert isinstance(geo_data, pd.DataFrame), "Geo data should be a pandas DataFrame"
    except Exception as e:
        pytest.fail(f"load_data raised an exception: {e}")
