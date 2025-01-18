import os
import pandas as pd
import streamlit as st
from typing import Tuple

class DataService:
    @staticmethod
    @st.cache_data
    def load_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Loads and processes two datasets: a processed data CSV and a geo data CSV.

        :return: A tuple containing two DataFrames:
            - The first DataFrame contains the processed data with latitude and longitude.
            - The second DataFrame contains the geo data with postal codes.
        """
        # Get the root directory of the project
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Construct absolute paths
        processed_data_path = os.path.join(root_dir, "datasets", "processed_data.csv")
        geo_data_path = os.path.join(root_dir, "datasets", "geodata_berlin_plz.csv")
        
        # Load the datasets
        data: pd.DataFrame = pd.read_csv(processed_data_path)
        data.rename(columns={"Breitengrad": "Latitude", "Längengrad": "Longitude"}, inplace=True)
        
        geo_data: pd.DataFrame = pd.read_csv(geo_data_path, delimiter=';')
        geo_data['plz'] = geo_data['PLZ'].astype(int)
        
        return data, geo_data
