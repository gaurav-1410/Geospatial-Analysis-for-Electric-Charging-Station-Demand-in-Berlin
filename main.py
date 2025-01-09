import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
import geopy.distance
from streamlit_folium import st_folium
from branca.colormap import LinearColormap
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
import os
import warnings
warnings.filterwarnings("ignore", category=UserWarning)


st.set_page_config(
    page_title="Berlin EV Charging Station Analysis",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <meta name="description" content="Analyze electric vehicle charging station demand in Berlin.">
    <meta name="keywords" content="Streamlit, Electric Vehicles, Charging Stations, Berlin, Data Analysis">
    """,
    unsafe_allow_html=True
)

firebase_creds = st.secrets["firebase"]
if not firebase_admin._apps:
    cred = credentials.Certificate(dict(firebase_creds))
    firebase_admin.initialize_app(cred)

class DataService:
    @st.cache_data
    def load_data(_self):
        data = pd.read_csv("datasets/processed_data.csv")
        data.rename(columns={"Breitengrad": "Latitude", "Längengrad": "Longitude"}, inplace=True)
        geo_data = pd.read_csv("datasets/geodata_berlin_plz.csv", delimiter=';')
        geo_data['plz'] = geo_data['PLZ'].astype(int)
        return data, geo_data


class FirebaseService:
    def __init__(self):
        load_dotenv()
        cred_path = os.getenv('FIREBASE_CREDENTIALS_PATH')
        if cred_path and not firebase_admin._apps:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def save_feedback(self, pincode, user_id, name, rating, feedback):
        feedback_collection = self.db.collection("feedback")
        query = feedback_collection.where("Pincode", "==", pincode).where("UserID", "==", user_id).get()

        if query:
            doc_id = query[0].id
            feedback_collection.document(doc_id).update({
                "Name": name,
                "Rating": rating,
                "Feedback": feedback,
            })
            st.success(f"Updated your feedback for Pincode: {pincode}")
        else:
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
    
    @staticmethod
    def find_nearby_stations(data, target_lat, target_lon, radius_km=2):
        def calculate_distance(row):
            return geopy.distance.geodesic(
                (row["Latitude"], row["Longitude"]), (target_lat, target_lon)
            ).km

        data["Distance"] = data.apply(calculate_distance, axis=1)
        return data[data["Distance"] <= radius_km]


# Initialize services
data_service = DataService()
firebase_service = FirebaseService()
map_service = MapService()

# Load data
data, geo_data = data_service.load_data()
geo_merged = geo_data.merge(data, on="plz", how="left")
geo_merged = gpd.GeoDataFrame(
    geo_merged, geometry=gpd.GeoSeries.from_wkt(geo_merged['geometry'])
)
geo_merged.set_crs("EPSG:4326", inplace=True)

pincode_suggestions = geo_merged['plz'].dropna().unique().tolist()

# Sidebar UI
selected_layer = st.sidebar.radio("Select Saerch by", ("Residents", "Charging Stations"))
intervals = st.sidebar.slider("Number of Legend Intervals", 3, 10, 5)

search_pincode = st.sidebar.selectbox(
    "Search by Pincode (e.g., 10115):",
    options=[""] + sorted(map(str, pincode_suggestions)),
    format_func=lambda x: x if x else "Enter or select a Pincode"
)

# Main section
st.title("⚡ Berlin Electric Charging Station Demand")
st.write("Visualize demand for electric vehicle charging stations in Berlin.")

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
<<<<<<< HEAD
    st.info("Adjust filters or enter a valid pincode.")
=======
    st.info("Adjust filters or enter a valid pincode.")

# Feedback section
if search_pincode:
    try:
        search_pincode = int(search_pincode)
        filtered_data = geo_merged[geo_merged['plz'] == search_pincode]
        if not filtered_data.empty:
            target_lat = filtered_data.iloc[0]["Latitude"]
            target_lon = filtered_data.iloc[0]["Longitude"]

            # Find nearby charging stations
            nearby_stations = map_service.find_nearby_stations(data, target_lat, target_lon)

            # Display map with markers for nearby charging stations
            st.subheader(f"Charging stations available near {search_pincode}")
            m = folium.Map(location=[target_lat, target_lon], zoom_start=13)
            for _, station in nearby_stations.iterrows():
                folium.Marker(
                    location=[station["Latitude"], station["Longitude"]],
                    popup=f"Station: {station['plz']}<br>Distance: {station['Distance']:.2f} km",
                    icon=folium.Icon(color="green", icon="bolt", prefix="fa"),
                ).add_to(m)

            # Add the map to Streamlit
            st_folium(m, width=700, height=500)

            # Feedback form
            st.sidebar.subheader(f"Feedback for Charging Stations at {search_pincode}")
            with st.sidebar.form("feedback_form"):
                user_id = st.text_input("Enter your UserID:")
                name = st.text_input("Enter your Name:")
                rating = st.slider("Rate the Charging Station (1-5):", 1, 5, 3)
                feedback_text = st.text_area("Enter your feedback for the selected station:")
                submit_button = st.form_submit_button("Submit Feedback")
                if submit_button:
                    if not user_id.strip() or not name.strip():
                        st.warning("UserID and Name are required.")
                    elif not feedback_text.strip():
                        st.warning("Feedback cannot be empty.")
                    else:
                        firebase_service.save_feedback(
                            pincode=search_pincode,
                            user_id=user_id.strip(),
                            name=name.strip(),
                            rating=rating,
                            feedback=feedback_text.strip(),
                        )
        else:
            st.warning(f"No data found for Pincode: {search_pincode}")
    except ValueError:
        st.error("Please enter a valid numeric pincode.")
else:
    st.info("Please select a pincode to view charging stations and provide feedback.")
>>>>>>> 9b18e5563e9fc54707ce883ce1fe0a8ebb5100d0
