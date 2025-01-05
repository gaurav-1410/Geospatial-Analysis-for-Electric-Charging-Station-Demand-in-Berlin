import pandas as pd
import geopandas as gpd

class DataPreprocessor:
    def __init__(self, population_file, charging_file, geo_file):
        self.population_file = population_file
        self.charging_file = charging_file
        self.geo_file = geo_file

    def load_population_data(self):
        data = pd.read_csv(self.population_file)
        data.rename(columns={"plz": "PLZ", "einwohner": "Population"}, inplace=True)
        return data

    def load_charging_data(self):
        data = pd.read_excel(self.charging_file)
        data.rename(columns={"Postleitzahl": "PLZ", "Nennleistung Ladeeinrichtung [kW]": "KW"}, inplace=True)
        data['Breitengrad'] = data['Breitengrad'].astype(str).str.replace(',', '.')
        data['Längengrad'] = data['Längengrad'].astype(str).str.replace(',', '.')
        return data

    def load_geo_data(self):
        data = pd.read_csv(self.geo_file, delimiter=';')
        data.rename(columns={"plz": "PLZ"}, inplace=True)
        return gpd.GeoDataFrame(data, geometry=gpd.GeoSeries.from_wkt(data['geometry']))

    def merge_data(self, population_data, charging_data, geo_data):
        charging_counts = charging_data.groupby("PLZ").size().reset_index(name='ChargingStations')
        merged = population_data.merge(charging_data, on="PLZ", how="left")
        if "Einwohner" not in merged.columns:
            merged["Einwohner"] = 0
        if "ChargingStations" in merged.columns:
            merged["ChargingStations"] = merged["ChargingStations"].fillna(0)
        else:
            merged["ChargingStations"] = 0
        merged["ChargingStations"] = merged["ChargingStations"].fillna(0)
        merged["PopulationPerStation"] = merged["Population"] / (merged["ChargingStations"] + 1)
        geo_merged = merged.merge(geo_data, on="PLZ", how="left")
        geo_merged = gpd.GeoDataFrame(geo_merged, geometry=geo_merged['geometry'])
        geo_merged.set_crs("EPSG:4326", inplace=True)
        return geo_merged
