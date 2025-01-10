import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

firebase_creds = st.secrets["firebase"]
if not firebase_admin._apps:
    cred = credentials.Certificate(dict(firebase_creds))
    firebase_admin.initialize_app(cred)

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