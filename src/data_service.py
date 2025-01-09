# import pandas as pd
# from streamlit import cache_data
# import streamlit as st

# class DataService:
#     @staticmethod
#     @st.cache_data
#     def load_data():
#         data = pd.read_csv("../datasets/processed_data.csv")
#         data.rename(columns={"Breitengrad": "Latitude", "Längengrad": "Longitude"}, inplace=True)
#         geo_data = pd.read_csv("../datasets/geodata_berlin_plz.csv", delimiter=';')
#         geo_data['plz'] = geo_data['PLZ'].astype(int)
#         return data, geo_data

import os
import pandas as pd
import streamlit as st

class DataService:
    @staticmethod
    @st.cache_data
    def load_data():
        # Get the root directory of the project
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Construct absolute paths
        processed_data_path = os.path.join(root_dir, "datasets", "processed_data.csv")
        geo_data_path = os.path.join(root_dir, "datasets", "geodata_berlin_plz.csv")
        
        # Load the datasets
        data = pd.read_csv(processed_data_path)
        data.rename(columns={"Breitengrad": "Latitude", "Längengrad": "Longitude"}, inplace=True)
        geo_data = pd.read_csv(geo_data_path, delimiter=';')
        geo_data['plz'] = geo_data['PLZ'].astype(int)
        
        return data, geo_data
