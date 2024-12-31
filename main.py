import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from branca.colormap import LinearColormap

# Cache data loading to improve performance
@st.cache_data
def load_data():
    data = pd.read_csv("datasets/processed_data.csv")
    geo_data = pd.read_csv("datasets/geodata_berlin_plz.csv", delimiter=';')
    geo_data['plz'] = geo_data['PLZ'].astype(int)
    return data, geo_data

data, geo_data = load_data()

# Merge geospatial and processed data
geo_merged = geo_data.merge(data, on="plz", how="left")
geo_merged = gpd.GeoDataFrame(
    geo_merged, geometry=gpd.GeoSeries.from_wkt(geo_merged['geometry'])
)
geo_merged.set_crs("EPSG:4326", inplace=True)

# Extract unique pincodes for suggestions
pincode_suggestions = geo_merged['plz'].dropna().unique().tolist()

def create_map(layer, gdf, intervals):
    """Generates a Folium map based on the selected data layer."""
    col = "Einwohner" if layer == "Residents" else "ChargingStations"
    color_map = LinearColormap(
        colors=["yellow", "red"],
        vmin=gdf[col].min(),
        vmax=gdf[col].max(),
        caption=layer,
    ).to_step(n=intervals)

    # Configure map
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

# Streamlit UI
st.title("Berlin Electric Charging Station Demand")
st.write("Visualize demand for electric vehicle charging stations in Berlin.")

selected_layer = st.radio("Select Data Layer", ("Residents", "Charging Stations"))
intervals = st.slider("Number of Legend Intervals", 3, 10, 5)

# Add a search bar with suggestions for pincodes
search_pincode = st.selectbox(
    "Search by Pincode (e.g., 10115):",
    options=[""] + sorted(map(str, pincode_suggestions)),  # Add an empty option for no selection
    format_func=lambda x: x if x else "Enter or select a Pincode"
)

# Filter data based on pincode
filtered_data = geo_merged
if search_pincode:
    try:
        search_pincode = int(search_pincode)
        filtered_data = geo_merged[geo_merged['plz'] == search_pincode]
        if filtered_data.empty:
            st.warning(f"No data found for Pincode: {search_pincode}")
            filtered_data = None
    except ValueError:
        st.error("Please enter a valid numeric pincode.")
        filtered_data = None

# Display map
if filtered_data is not None and not filtered_data.empty:
    map_ = create_map(selected_layer, filtered_data, intervals)
    st_folium(map_, width=700, height=500)
else:
    st.info("Adjust filters or enter a valid pincode.")