import pytest
import sys
import os
from unittest import mock
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from src.data_service import DataService

# Mock dataset paths
@pytest.fixture
def mock_dataset_path():
    # Mocking the behavior of the load_data method
    with mock.patch('src.data_service.DataService.load_data', return_value=(["mocked_data"], ["mocked_geo_data"])):
        yield

def test_load_data(mock_dataset_path):
    # Initialize the DataService
    data_service = DataService()
    try:
        # Call the load_data method
        data, geo_data = data_service.load_data()
        
        # Assert the mocked return values
        assert data == ["mocked_data"], "Data should match the mocked return value"
        assert geo_data == ["mocked_geo_data"], "Geo data should match the mocked return value"
    except Exception as e:
        pytest.fail(f"load_data raised an exception: {e}")
