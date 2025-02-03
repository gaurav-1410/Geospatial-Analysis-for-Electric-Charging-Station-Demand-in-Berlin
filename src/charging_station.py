from typing import List

class ChargingStation:
    def __init__(self, station_id, postal_code, latitude, longitude):
        self.station_id = station_id
        self.postal_code = postal_code
        self.latitude = latitude
        self.longitude = longitude
        self.feedbacks = []
    
    def get_station_id(self):
        return self.station_id

    def add_feedback(self, feedback: str) -> None:
        """
        Adds a feedback to the list of feedbacks for the station.

        :param feedback: A string containing the feedback to be added.
        """
        self.feedbacks.append(feedback)