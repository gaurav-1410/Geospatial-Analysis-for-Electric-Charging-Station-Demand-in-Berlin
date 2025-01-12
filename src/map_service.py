import folium
from branca.colormap import LinearColormap
from chargingstation import ChargingStation
import geopy.distance
import pandas as pd

class MapService:
    station_id_counter = 0

    @staticmethod
    def create_map(layer, gdf, intervals):
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
    def find_nearby_stations(data, target_lat, target_lon, radius_km=2):
        def calculate_distance(row):
            return geopy.distance.geodesic(
                (row["Latitude"], row["Longitude"]), (target_lat, target_lon)
            ).km

        data["Distance"] = data.apply(calculate_distance, axis=1)
        return data[data["Distance"] <= radius_km]

    @staticmethod
    def organize_stations_by_area(data):
        from area import Area
        areas = {}

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

            areas[postal_code].addChargingStation(station)

        return areas

    @staticmethod
    def find_area_by_pincode(areas, pincode):
        return areas.get(pincode, None)