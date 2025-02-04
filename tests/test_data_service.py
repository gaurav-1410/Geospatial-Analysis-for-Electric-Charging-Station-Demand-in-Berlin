import pytest
import sys
import os
import pandas as pd
from unittest import mock
from typing import Tuple
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from src.Infrastructure.data_service import DataService

def test_load_data_real() -> None:
    """
    Test the `load_data` method of the `DataService` class to ensure it returns
    two pandas DataFrame objects (`data` and `geo_data`) and handles exceptions.

    :return: None
    """
    data_service = DataService()

    try:
        # Load data and geo data
        data, geo_data = data_service.load_data()

        # Assert both dataframes are loaded correctly
        assert isinstance(data, pd.DataFrame), "Data should be a pandas DataFrame"
        assert isinstance(geo_data, pd.DataFrame), "Geo data should be a pandas DataFrame"

    except Exception as e:
        pytest.fail(f"load_data raised an exception: {e}")
