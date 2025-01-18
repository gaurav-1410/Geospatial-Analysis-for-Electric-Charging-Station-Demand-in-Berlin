from typing import List, Dict, Optional

class FeedbackService:
    def __init__(self) -> None:
        """
        Initializes a FeedbackService object with empty dictionaries to store feedbacks by station and user.
        """
        self.feedbacks_by_station: Dict[str, List[Dict[str, str]]] = {}
        self.feedbacks_by_user: Dict[str, List[Dict[str, str]]] = {}

    def add_feedback(self, station_id: str, user_id: str, name: str, rating: int, feedback_text: str) -> None:
        """
        Adds feedback for a specific station and user.

        :param station_id: The ID of the charging station.
        :param user_id: The ID of the user providing the feedback.
        :param name: The name of the user providing the feedback.
        :param rating: The rating given by the user (typically an integer).
        :param feedback_text: The text of the user's feedback.
        """
        feedback_entry = {
            "user_id": user_id,
            "name": name,
            "rating": rating,
            "feedback": feedback_text
        }

        # Add feedback to the station's list
        if station_id not in self.feedbacks_by_station:
            self.feedbacks_by_station[station_id] = []
        self.feedbacks_by_station[station_id].append(feedback_entry)

        # Add feedback to the user's list
        if user_id not in self.feedbacks_by_user:
            self.feedbacks_by_user[user_id] = []
        self.feedbacks_by_user[user_id].append({"station_id": station_id, **feedback_entry})

    def get_feedbacks_for_station(self, station_id: str) -> List[Dict[str, str]]:
        """
        Retrieves all feedback for a given station.

        :param station_id: The ID of the station for which feedbacks are requested.
        :return: A list of feedback entries associated with the given station.
        """
        return self.feedbacks_by_station.get(station_id, [])

    def get_feedbacks_by_user(self, user_id: str) -> List[Dict[str, str]]:
        """
        Retrieves all feedback provided by a specific user.

        :param user_id: The ID of the user for which feedbacks are requested.
        :return: A list of feedback entries provided by the user.
        """
        return self.feedbacks_by_user.get(user_id, [])
