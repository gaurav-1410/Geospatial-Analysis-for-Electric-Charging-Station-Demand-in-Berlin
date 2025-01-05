import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from branca.colormap import LinearColormap
import firebase_admin
from firebase_admin import credentials, firestore
import os
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

class FirebaseService:
    def __init__(self):
        cred_path = os.getenv('FIREBASE_CREDENTIALS_PATH')
        if cred_path and not firebase_admin._apps:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()

class DataService:
    @st.cache_data
    def load_data(_self):
        data = pd.read_csv("datasets/processed_data.csv")
        geo_data = pd.read_csv("datasets/geodata_berlin_plz.csv", delimiter=';')
        geo_data['plz'] = geo_data['PLZ'].astype(int)
        return data, geo_data


# export FIREBASE_CREDENTIALS_PATH="/path/to/your/firebase_credentials.json"

class FirebaseService:
    def __init__(self, cred_path):
        if not firebase_admin._apps:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def save_feedback(self, pincode, user_id, name, rating, feedback):
        feedback_collection = self.db.collection("feedback")
        query = feedback_collection.where("Pincode", "==", pincode).where("UserID", "==", user_id).get()

        if query:  # Update existing feedback
            doc_id = query[0].id
            feedback_collection.document(doc_id).update({
                "Name": name,
                "Rating": rating,
                "Feedback": feedback,
            })
            st.success(f"Updated your feedback for Pincode: {pincode}")
        else:  # Create new feedback
            feedback_data = {
                "Pincode": pincode,
                "UserID": user_id,
                "Name": name,
                "Rating": rating,
                "Feedback": feedback,
            }
            feedback_collection.add(feedback_data)
            st.success(f"Thank you for your feedback for Pincode: {pincode}")


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


# Initialize services
data_service = DataService()
firebase_service = FirebaseService("firebase_credentials.json")
map_service = MapService()

# Load data
data, geo_data = data_service.load_data()
geo_merged = geo_data.merge(data, on="plz", how="left")
geo_merged = gpd.GeoDataFrame(
    geo_merged, geometry=gpd.GeoSeries.from_wkt(geo_merged['geometry'])
)
geo_merged.set_crs("EPSG:4326", inplace=True)

pincode_suggestions = geo_merged['plz'].dropna().unique().tolist()

# Streamlit UI
st.title("Berlin Electric Charging Station Demand")
st.write("Visualize demand for electric vehicle charging stations in Berlin.")

selected_layer = st.radio("Select Data Layer", ("Residents", "Charging Stations"))
intervals = st.slider("Number of Legend Intervals", 3, 10, 5)

search_pincode = st.selectbox(
    "Search by Pincode (e.g., 10115):",
    options=[""] + sorted(map(str, pincode_suggestions)),
    format_func=lambda x: x if x else "Enter or select a Pincode"
)

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

if filtered_data is not None and not filtered_data.empty:
    map_ = map_service.create_map(selected_layer, filtered_data, intervals)
    st_folium(map_, width=700, height=500)
else:
    st.info("Adjust filters or enter a valid pincode.")

# Feedback section
st.header("Provide Feedback for Charging Stations")
if search_pincode:
    with st.form("feedback_form"):
        user_id = st.text_input("Enter your UserID:")
        name = st.text_input("Enter your Name:")
        rating = st.slider("Rate the Charging Stations (1-5):", 1, 5, 3)
        feedback_text = st.text_area("Enter your feedback for the selected pincode:")
        submit_button = st.form_submit_button("Submit Feedback")
        if submit_button:
            if not user_id.strip() or not name.strip():
                st.warning("UserID and Name are required.")
            elif not feedback_text.strip():
                st.warning("Feedback cannot be empty.")
            else:
                firebase_service.save_feedback(search_pincode, user_id.strip(), name.strip(), rating, feedback_text.strip())
else:
    st.info("Please select a pincode to provide feedback.")
