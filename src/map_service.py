import folium
from branca.colormap import LinearColormap
import geopy.distance
import pandas as pd

class MapService:
    @staticmethod
    def create_map(layer, gdf, intervals):
        col = "Einwohner" if layer == "Residents" else "ChargingStations"
        color_map = LinearColormap(
            colors=["yellow", "red"],
            vmin=gdf[col].min(),
            vmax=gdf[col].max(),
            caption=layer,
        ).to_step(n=intervals)

        m = folium.Map(location=[52.52, 13.42], zoom_start=10)
        folium.GeoJson(
            gdf,
            style_function=lambda feature: {
                "fillColor": color_map(feature["properties"][col]),
                "color": "black",
                "weight": 1,
                "fillOpacity": 0.7,
            },
            tooltip=folium.features.GeoJsonTooltip(
                fields=["plz", col],
                aliases=["Pincode", layer],
            ),
        ).add_to(m)
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
