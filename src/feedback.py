class FeedbackService:
    def __init__(self):
        self.feedbacks_by_station = {}
        self.feedbacks_by_user = {}

    def add_feedback(self, station_id, user_id, name, rating, feedback_text):
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

    def get_feedbacks_for_station(self, station_id):
        return self.feedbacks_by_station.get(station_id, [])

    def get_feedbacks_by_user(self, user_id):
        return self.feedbacks_by_user.get(user_id, [])
