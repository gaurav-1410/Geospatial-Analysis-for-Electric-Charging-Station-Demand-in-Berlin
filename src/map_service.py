import folium
from branca.colormap import LinearColormap
from charging_station import ChargingStation
import geopy.distance
import pandas as pd
from area import Area
from typing import Dict, Optional

class MapService:
    station_id_counter: int = 0

    @staticmethod
    def create_map(layer: str, gdf: pd.DataFrame, intervals: int) -> folium.Map:
        """
        Creates a choropleth map using the given layer and GeoDataFrame.

        :param layer: The type of layer to visualize (e.g., "Residents" or "ChargingStations").
        :param gdf: The GeoDataFrame containing the data to visualize.
        :param intervals: The number of intervals for the color map.
        :return: A folium Map object with the choropleth layer.
        """
        # Determine the column to visualize
        col = "Einwohner" if layer == "Residents" else "ChargingStations"

        # Create a color map
        color_map = LinearColormap(
            colors=["yellow", "orange", "red"],
            vmin=gdf[col].min(),
            vmax=gdf[col].max(),
            caption=layer
        ).to_step(n=intervals)

        # Initialize a folium map
        m = folium.Map(location=[52.52, 13.42], zoom_start=10)

        # Add GeoJSON layer for choropleth visualization
        folium.GeoJson(
            gdf,
            style_function=lambda feature: {
                "fillColor": color_map(feature["properties"][col]),
                "color": "black",
                "weight": 1,
                "fillOpacity": 0.7,
            },
            tooltip=folium.features.GeoJsonTooltip(
                fields=["PLZ", col],
                aliases=["Pincode", layer],
            ),
        ).add_to(m)

        # Add the color map legend
        color_map.add_to(m)

        return m

    @staticmethod
    def find_nearby_stations(data: pd.DataFrame, target_lat: float, target_lon: float, radius_km: float = 2) -> pd.DataFrame:
        """
        Finds charging stations within a specified radius of the target coordinates.

        :param data: The DataFrame containing charging station data.
        :param target_lat: The latitude of the target location.
        :param target_lon: The longitude of the target location.
        :param radius_km: The radius in kilometers within which to search for stations.
        :return: A DataFrame containing stations within the specified radius.
        """
        def calculate_distance(row: pd.Series) -> float:
            return geopy.distance.geodesic(
                (row["Latitude"], row["Longitude"]), (target_lat, target_lon)
            ).km

        data["Distance"] = data.apply(calculate_distance, axis=1)
        return data[data["Distance"] <= radius_km]

    @staticmethod
    def organize_stations_by_area(data: pd.DataFrame) -> Dict[str, Area]:
        """
        Organizes charging stations into areas based on postal codes.

        :param data: The DataFrame containing charging station data.
        :return: A dictionary where the keys are postal codes and the values are Area objects.
        """
        from area import Area
        areas: Dict[str, Area] = {}

        for _, row in data.iterrows():
            postal_code = row['plz']
            latitude = row['Latitude']
            longitude = row['Longitude']

            if postal_code not in areas:
                areas[postal_code] = Area(postal_code)

            station = ChargingStation(
                station_id=MapService.station_id_counter,
                postal_code=postal_code,
                latitude=latitude,
                longitude=longitude
            )
            MapService.station_id_counter += 1

            areas[postal_code].add_charging_station(station)

        return areas

    @staticmethod
    def find_area_by_pincode(areas: Dict[str, Area], pincode: str) -> Optional[Area]:
        """
        Finds an area by its postal code.

        :param areas: A dictionary of areas indexed by postal code.
        :param pincode: The postal code of the area to find.
        :return: The Area object if found, otherwise None.
        """
        return areas.get(pincode, None)
