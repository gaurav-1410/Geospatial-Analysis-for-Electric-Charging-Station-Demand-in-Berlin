import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from branca.colormap import LinearColormap

# Cache data loading to improve performance
@st.cache_data
def load_data():
    # Load processed data
    data = pd.read_csv("datasets/processed_data.csv")

    # Load geospatial data
    geo_data = pd.read_csv("datasets/geodata_berlin_plz.csv", delimiter=';')
    geo_data['plz'] = geo_data['PLZ'].astype(int)  # Ensure postal codes are integers.

    return data, geo_data

data, geo_data = load_data()

# Merge the geospatial and processed data for visualization
geo_merged = geo_data.merge(data, on="plz", how="left")  # Perform a left join to keep all geospatial areas.
geo_merged = gpd.GeoDataFrame(
    geo_merged,
    geometry=gpd.GeoSeries.from_wkt(geo_merged['geometry'])  # Convert geometry strings to GeoSeries.")
)

# Ensure Coordinate Reference System (CRS) is set correctly.
# Berlin uses the WGS 84 CRS (EPSG:4326).
if geo_merged.crs is None:
    geo_merged.set_crs("EPSG:4326", inplace=True)

# Function to create the map with a detailed legend
def create_map(selected_layer, data, intervals=5):
    """
    Create an interactive map displaying data for Berlin postal codes.

    Parameters:
    - selected_layer: The data layer to visualize ('Residents' or 'Charging Stations').
    - data: GeoDataFrame containing geospatial and metric data.
    - intervals: Number of intervals for the color map legend.

    Returns:
    - folium.Map object with the selected data layer visualized.
    """
    # Initialize the map centered on Berlin with a default zoom level.
    m = folium.Map(location=[52.52, 13.42], zoom_start=10)

    # Configure the color map and column based on the selected data layer.
    if selected_layer == "Residents":
        col = 'Einwohner'  # Column for resident data.
        color_map = LinearColormap(
            colors=['yellow', 'red'],  # Gradient from yellow to red.
            vmin=data[col].min(),  # Minimum value for the color scale.
            vmax=data[col].max(),  # Maximum value for the color scale.
            caption="Residents"  # Legend caption.
        ).to_step(n=intervals)  # Adjust intervals dynamically.
    elif selected_layer == "Charging Stations":
        col = 'ChargingStations'  # Column for charging station data.
        color_map = LinearColormap(
            colors=['yellow', 'red'],
            vmin=data[col].min(),
            vmax=data[col].max(),
            caption="Charging Stations"
        ).to_step(n=intervals)

    # Add a GeoJSON layer with styling and tooltips.
    folium.GeoJson(
        data,
        style_function=lambda feature: {
            'fillColor': color_map(feature['properties'][col]),  # Color based on value.
            'color': 'black',  # Outline color.
            'weight': 1,  # Outline width.
            'fillOpacity': 0.7  # Fill transparency.
        },
        tooltip=folium.features.GeoJsonTooltip(
            fields=['plz', col],  # Fields to display in the tooltip.
            aliases=['Pincode', selected_layer],  # Custom labels for the fields.
            localize=True  # Format numbers and dates.
        )
    ).add_to(m)

    # Add the color map legend to the map.
    color_map.add_to(m)

    return m

# Streamlit app layout
st.title("Berlin Electric Charging Station Demand")

st.write(
    "This app visualizes demand for electric vehicle charging stations in Berlin. "
    "Use the radio buttons below to switch between viewing 'Residents' or 'Charging Stations' data."
)

# Add radio buttons for user to select the data layer to display.
selected_layer = st.radio("Select Data Layer", ("Residents", "Charging Stations"))

# Add a slider for dynamic interval adjustment.
intervals = st.slider("Number of Legend Intervals", min_value=3, max_value=10, value=5)

# Add a search bar for filtering by postal code (pincode).
search_pincode = st.text_input("Search by Pincode (e.g., 10115):")

# Filter the data based on the entered postal code.
if search_pincode:
    try:
        search_pincode = int(search_pincode)  # Ensure the input is a valid integer.
        filtered_data = geo_merged[geo_merged['plz'] == search_pincode]  # Filter rows by pincode.
        if filtered_data.empty:
            st.warning(f"No data found for Pincode: {search_pincode}")
        else:
            st.success(f"Showing data for Pincode: {search_pincode}")
    except ValueError:
        st.error("Please enter a valid numeric pincode.")
else:
    filtered_data = geo_merged  # Show all data if no pincode is entered.

# Provide an option to download the filtered data.
# st.download_button(
#     label="Download Filtered Data",
#     data=filtered_data.to_csv(index=False),
#     file_name="filtered_data.csv",
#     mime="text/csv"
# )

# Create the map with the selected data layer and filtered data.
map_ = create_map(selected_layer, filtered_data, intervals=intervals)

# Display the map using Streamlit's folium integration.
st_folium(map_, width=700, height=500)