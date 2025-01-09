import pandas as pd
from streamlit import cache_data
import streamlit as st

class DataService:
    @staticmethod
    @st.cache_data
    def load_data():
        data = pd.read_csv("../datasets/processed_data.csv")
        data.rename(columns={"Breitengrad": "Latitude", "Längengrad": "Longitude"}, inplace=True)
        geo_data = pd.read_csv("../datasets/geodata_berlin_plz.csv", delimiter=';')
        geo_data['plz'] = geo_data['PLZ'].astype(int)
        return data, geo_data
