import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from branca.colormap import LinearColormap

# Load processed data
data = pd.read_csv("processed_data.csv")

# Load geospatial data
geo_data = gpd.read_file("plz-5stellig.geojson")

# Merge data for visualization
geo_data['plz'] = geo_data['plz'].astype(int)
geo_merged = geo_data.merge(data, on="plz", how="left")
geo_merged = geo_merged[(geo_merged.plz > 10000) & (geo_merged.plz < 14200)]

# Function to create the map with different layers
def create_map(selected_layer):
    m = folium.Map(location=[52.52, 13.42], zoom_start=10)
    
    # Define the layer to display based on user selection
    if selected_layer == "Residents":
        color_map = LinearColormap(colors=['yellow', 'red'], vmin=geo_merged['Einwohner'].min(), vmax=geo_merged['Einwohner'].max())

        for idx, row in geo_merged.iterrows():
            folium.GeoJson(
                row['geometry'],
                style_function=lambda x, color=color_map(row['Einwohner']): {
                    'fillColor': color,
                    'color': 'black',
                    'weight': 1,
                    'fillOpacity': 0.7
                },
                tooltip=f"PLZ: {row['plz']} - Einwohner: {row['Einwohner']}" 
            ).add_to(m)

        # data_to_display = geo_merged[['plz', 'einwohner', 'geometry']]
        popup_column = 'einwohner'
        legend_name = "Residents"
        # fill_color = color  # Red for charging station density
        
    
    elif selected_layer == "Charging Stations":
        color_map = LinearColormap(colors=['yellow', 'red'], vmin=geo_merged['ChargingStations'].min(), vmax=geo_merged['ChargingStations'].max())

        for idx, row in geo_merged.iterrows():
            folium.GeoJson(
                row['geometry'],
                style_function=lambda x, color=color_map(row['ChargingStations']): {
                    'fillColor': color,
                    'color': 'black',
                    'weight': 1,
                    'fillOpacity': 0.7
                },
                tooltip=f"PLZ: {row['plz']}, ChargingStations: {row['ChargingStations']}" 
            ).add_to(m)

        # data_to_display = geo_merged[['plz', 'ChargingStations', 'geometry']]
        popup_column = 'ChargingStations'
        legend_name = "Charging Stations"
        # fill_color =   # Red for charging station density

    # Add choropleth layer to the map
    folium.Choropleth(
        geo_data=geo_merged,
        data=geo_merged,
        columns=["plz", popup_column],
        key_on="feature.properties.plz",
        fill_color="YlOrRd",
        fill_opacity=0.4,
        line_opacity=0.9,
        legend_name=legend_name
    ).add_to(m)
    
    # Add popups to show relevant information when hovering over regions
    for _, row in geo_merged.iterrows():
        folium.GeoJson(
            row['geometry'],
            style_function=lambda x, color=color_map(row[popup_column]): {
            'fillColor': color,
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.7
        },
        highlight_function=lambda x: {
            'weight': 3,         # Border thickness on hover
            'color': 'black',    # Border color on hover
            'fillOpacity': 0.9   # Fill opacity on hover
        },
            tooltip=f"Pincode: {row['plz']} - {legend_name}: {row[popup_column]}",
            popup=f"Pincode: {row['plz']}<br>{popup_column}: {row[popup_column]}"
        ).add_to(m)

    return m

# Streamlit app layout
st.title("Berlin Electric Charging Station Demand")

st.write("This app visualizes demand for electric vehicle charging stations in Berlin. Use the radio buttons below to switch between viewing 'Residents' or 'Charging Stations' data.")

# Add radio buttons for user to select the layer
selected_layer = st.radio("Select Data Layer", ("Residents", "Charging Stations"))

# Note
st.write('''(Note: Layer switching takes time.)''')

# Create and display the map based on the selected layer
map_ = create_map(selected_layer)
st_folium(map_, width=700, height=500)
