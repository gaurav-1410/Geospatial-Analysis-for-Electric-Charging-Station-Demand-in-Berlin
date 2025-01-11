# import streamlit as st
# import folium
# from data_service import DataService
# from firebase_service import FirebaseService
# from map_service import MapService
# import geopandas as gpd
# import pandas as pd
# from streamlit_folium import st_folium

# st.set_page_config(
#     page_title="Berlin EV Charging Station Analysis",
#     page_icon="⚡",
#     layout="centered",
#     initial_sidebar_state="collapsed",
# )

# st.markdown(
#     """
#     <meta name="description" content="Analyze electric vehicle charging station demand in Berlin.">
#     <meta name="keywords" content="Streamlit, Electric Vehicles, Charging Stations, Berlin, Data Analysis">
#     """,
#     unsafe_allow_html=True
# )

# # Initialize services
# data_service = DataService()
# firebase_service = FirebaseService()
# map_service = MapService()

# # Load data
# data, geo_data = data_service.load_data()
# geo_merged = geo_data.merge(data, on="plz", how="left")
# geo_merged = gpd.GeoDataFrame(
#     geo_merged, geometry=gpd.GeoSeries.from_wkt(geo_merged['geometry'])
# )
# geo_merged.set_crs("EPSG:4326", inplace=True)

# pincode_suggestions = geo_merged['plz'].dropna().unique().tolist()

# # Sidebar UI
# selected_layer = st.sidebar.radio("Select Search by", ("Residents", "Charging Stations"))
# intervals = st.sidebar.slider("Number of Legend Intervals", 3, 10, 5)

# search_pincode = st.sidebar.selectbox(
#     "Search by Pincode (e.g., 10115):",
#     options=[""] + sorted(map(str, pincode_suggestions)),
#     format_func=lambda x: x if x else "Enter or select a Pincode"
# )

# # Main section
# st.title("⚡ Berlin Electric Charging Station Demand")
# st.write("Visualize demand for electric vehicle charging stations in Berlin.")

# filtered_data = geo_merged
# if search_pincode:
#     try:
#         search_pincode = int(search_pincode)
#         filtered_data = geo_merged[geo_merged['plz'] == search_pincode]
#         if filtered_data.empty:
#             st.warning(f"No data found for Pincode: {search_pincode}")
#             filtered_data = None
#     except ValueError:
#         st.error("Please enter a valid numeric pincode.")
#         filtered_data = None

# if filtered_data is not None and not filtered_data.empty:
#     map_ = map_service.create_map(selected_layer, filtered_data, intervals)
#     st_folium(map_, width=700, height=500)
# else:
#     st.info("Adjust filters or enter a valid pincode.")

# # Feedback section
# if search_pincode:
#     try:
#         search_pincode = int(search_pincode)
#         filtered_data = geo_merged[geo_merged['plz'] == search_pincode]
#         if not filtered_data.empty:
#             target_lat = filtered_data.iloc[0]["Latitude"]
#             target_lon = filtered_data.iloc[0]["Longitude"]

#             # Find nearby charging stations
#             nearby_stations = map_service.find_nearby_stations(data, target_lat, target_lon)

#             # Display map with markers for nearby charging stations
#             st.subheader(f"Charging stations available near {search_pincode}")
#             m = folium.Map(location=[target_lat, target_lon], zoom_start=13)
#             for _, station in nearby_stations.iterrows():
#                 folium.Marker(
#                     location=[station["Latitude"], station["Longitude"]],
#                     popup=f"Station: {station['plz']}<br>Distance: {station['Distance']:.2f} km",
#                     icon=folium.Icon(color="green", icon="bolt", prefix="fa"),
#                 ).add_to(m)

#             # Add the map to Streamlit
#             st_folium(m, width=700, height=500)

#             # Feedback form
#             st.sidebar.subheader(f"Feedback for Charging Stations at {search_pincode}")
#             with st.sidebar.form("feedback_form"):
#                 user_id = st.text_input("Enter your UserID:")
#                 name = st.text_input("Enter your Name:")
#                 rating = st.slider("Rate the Charging Station (1-5):", 1, 5, 3)
#                 feedback_text = st.text_area("Enter your feedback for the selected station:")
#                 submit_button = st.form_submit_button("Submit Feedback")
#                 if submit_button:
#                     if not user_id.strip() or not name.strip():
#                         st.warning("UserID and Name are required.")
#                     elif not feedback_text.strip():
#                         st.warning("Feedback cannot be empty.")
#                     else:
#                         firebase_service.save_feedback(
#                             pincode=search_pincode,
#                             user_id=user_id.strip(),
#                             name=name.strip(),
#                             rating=rating,
#                             feedback=feedback_text.strip(),
#                         )
#         else:
#             st.warning(f"No data found for Pincode: {search_pincode}")
#     except ValueError:
#         st.error("Please enter a valid numeric pincode.")
# else:
#     st.info("Please select a pincode to view charging stations and provide feedback.")


import streamlit as st
import folium
from map_service import MapService
from Feedback import FeedbackService
import geopandas as gpd
from streamlit_folium import st_folium
import pandas as pd
from shapely.geometry import Point


feedback_service = FeedbackService()
map_service = MapService()

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

# Load data
data = pd.read_csv("datasets/processed_data.csv")  # Replace with actual dataset
geo_data = gpd.read_file("datasets/geodata_berlin_plz.csv")  # Replace with actual GeoJSON file
data.rename(columns={"Breitengrad": "Latitude", "Längengrad": "Longitude"}, inplace=True)
geo_data['plz'] = geo_data['PLZ'].astype(int)
geo_data = geo_data.merge(data, on="plz", how="left")
geo_data['geometry'] = geo_data.apply(lambda row: Point(row['Longitude'], row['Latitude']), axis=1)
geo_data = gpd.GeoDataFrame(geo_data, geometry='geometry')
geo_data.set_crs("EPSG:4326", inplace=True)

# Organize charging stations into areas by postal code
areas = map_service.organize_stations_by_area(data)
pincode_suggestions = areas.keys()

# Sidebar UI
selected_layer = st.sidebar.radio("Select Search by", ("Residents", "Charging Stations"))
intervals = st.sidebar.slider("Number of Legend Intervals", 3, 10, 5)
search_pincode = st.sidebar.selectbox(
    "Search by Pincode:",
    options=[""] + [int(code) for code in pincode_suggestions],
    format_func=lambda x: x if x else "Enter or select a Pincode"
)
search_station_id = st.sidebar.text_input("Enter Station ID (optional):")

# Main section
# Main section
st.title("⚡ Berlin Electric Charging Station Demand")
st.write("Visualize demand for electric vehicle charging stations in Berlin.")

# Default map showing all data
if not search_pincode:
    st.info("Enter a pincode to view specific data, or explore the entire map below.")
    
    # Display the full map
    map_ = map_service.create_map(selected_layer, geo_data, intervals)
    st_folium(map_, width=700, height=500)
else:
    # Existing code to handle specific pincode search
    try:
        pincode = int(search_pincode)
        area = map_service.find_area_by_pincode(areas, pincode)

        if area:
            st.write(f"Stations in Area: {pincode}")
            for station in area.stations:
                st.write(f"Station ID: {station.station_id}, Location: ({station.latitude}, {station.longitude})")

            # Handle specific station search
            if search_station_id:
                try:
                    station_id = int(search_station_id)
                    station = area.find_station_by_id(station_id)
                    if station:
                        st.success(f"Station Found: ID {station.id}, Location: ({station.latitude}, {station.longitude})")

                        # Display feedbacks for the station
                        st.subheader(f"Feedback for Station ID {station_id}")
                        feedbacks = feedback_service.get_feedbacks_for_station(station_id)
                        if feedbacks:
                            for feedback in feedbacks:
                                st.write(f"User: {feedback['name']} ({feedback['user_id']})")
                                st.write(f"Rating: {feedback['rating']}\nFeedback: {feedback['feedback']}")
                                st.write("---")
                        else:
                            st.write("No feedback available for this station.")
                    else:
                        st.warning(f"No station with ID {station_id} found in area {pincode}.")
                except ValueError:
                    st.error("Invalid Station ID. Please enter a numeric value.")

            # Display filtered map
            filtered_data = geo_data[geo_data['plz'] == pincode]
            if not filtered_data.empty:
                map_ = map_service.create_map(selected_layer, filtered_data, intervals)
                st_folium(map_, width=700, height=500)
            else:
                st.warning(f"No geographic data found for Pincode: {pincode}")

            # Feedback section
            st.sidebar.subheader(f"Feedback for Charging Stations at {pincode}")
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
                        feedback_service.add_feedback(
                            station_id=int(search_station_id) if search_station_id else None,
                            user_id=user_id.strip(),
                            name=name.strip(),
                            rating=rating,
                            feedback_text=feedback_text.strip(),
                        )
                        st.success(f"Thank you for your feedback, {name}!")
        else:
            st.warning(f"No area found for Pincode: {pincode}")
    except ValueError:
        st.error("Invalid Pincode. Please enter a numeric value.")


# import streamlit as st
# import folium
# from data_service import DataService
# from firebase_service import FirebaseService
# from map_service import MapService
# import geopandas as gpd
# import pandas as pd
# from streamlit_folium import st_folium

# st.set_page_config(
#     page_title="Berlin EV Charging Station Analysis",
#     page_icon="⚡",
#     layout="centered",
#     initial_sidebar_state="collapsed",
# )

# st.markdown(
#     """
#     <meta name="description" content="Analyze electric vehicle charging station demand in Berlin.">
#     <meta name="keywords" content="Streamlit, Electric Vehicles, Charging Stations, Berlin, Data Analysis">
#     """,
#     unsafe_allow_html=True
# )

# # Initialize services
# data_service = DataService()
# firebase_service = FirebaseService()
# map_service = MapService()

# # Load data
# data, geo_data = data_service.load_data()
# geo_merged = geo_data.merge(data, on="plz", how="left")
# geo_merged = gpd.GeoDataFrame(
#     geo_merged, geometry=gpd.GeoSeries.from_wkt(geo_merged['geometry'])
# )
# geo_merged.set_crs("EPSG:4326", inplace=True)

# pincode_suggestions = geo_merged['plz'].dropna().unique().tolist()

# # Sidebar UI
# selected_layer = st.sidebar.radio("Select Search by", ("Residents", "Charging Stations"))
# intervals = st.sidebar.slider("Number of Legend Intervals", 3, 10, 5)

# search_pincode = st.sidebar.selectbox(
#     "Search by Pincode (e.g., 10115):",
#     options=[""] + sorted(map(str, pincode_suggestions)),
#     format_func=lambda x: x if x else "Enter or select a Pincode"
# )

# # Main section
# st.title("⚡ Berlin Electric Charging Station Demand")
# st.write("Visualize demand for electric vehicle charging stations in Berlin.")

# # Default map display when no pincode is selected
# if not search_pincode:
#     st.info("Explore the map below or search by entering a pincode.")
#     map_ = map_service.create_map(selected_layer, geo_merged, intervals)
#     st_folium(map_, width=700, height=500)

# # Filtered map display when pincode is selected
# else:
#     try:
#         search_pincode = int(search_pincode)
#         filtered_data = geo_merged[geo_merged['plz'] == search_pincode]
#         if filtered_data.empty:
#             st.warning(f"No data found for Pincode: {search_pincode}")
#         else:
#             map_ = map_service.create_map(selected_layer, filtered_data, intervals)
#             st_folium(map_, width=700, height=500)

#             # Nearby charging stations
#             target_lat = filtered_data.iloc[0]["Latitude"]
#             target_lon = filtered_data.iloc[0]["Longitude"]

#             nearby_stations = map_service.find_nearby_stations(data, target_lat, target_lon)

#             # Map for nearby stations
#             st.subheader(f"Charging stations available near {search_pincode}")
#             m = folium.Map(location=[target_lat, target_lon], zoom_start=13)
#             for _, station in nearby_stations.iterrows():
#                 folium.Marker(
#                     location=[station["Latitude"], station["Longitude"]],
#                     popup=f"Station: {station['plz']}<br>Distance: {station['Distance']:.2f} km",
#                     icon=folium.Icon(color="green", icon="bolt", prefix="fa"),
#                 ).add_to(m)

#             st_folium(m, width=700, height=500)

#             # Feedback form
#             st.sidebar.subheader(f"Feedback for Charging Stations at {search_pincode}")
#             with st.sidebar.form("feedback_form"):
#                 user_id = st.text_input("Enter your UserID:")
#                 name = st.text_input("Enter your Name:")
#                 rating = st.slider("Rate the Charging Station (1-5):", 1, 5, 3)
#                 feedback_text = st.text_area("Enter your feedback for the selected station:")
#                 submit_button = st.form_submit_button("Submit Feedback")
#                 if submit_button:
#                     if not user_id.strip() or not name.strip():
#                         st.warning("UserID and Name are required.")
#                     elif not feedback_text.strip():
#                         st.warning("Feedback cannot be empty.")
#                     else:
#                         firebase_service.save_feedback(
#                             pincode=search_pincode,
#                             user_id=user_id.strip(),
#                             name=name.strip(),
#                             rating=rating,
#                             feedback=feedback_text.strip(),
#                         )
#     except ValueError:
#         st.error("Please enter a valid numeric pincode.")
