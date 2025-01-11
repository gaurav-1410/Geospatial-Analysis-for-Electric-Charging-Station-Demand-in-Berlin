# class Area:
#     pincode
#     chargingStations = []
    
#     def __init__(self, pincode):
#         self.pincode = pincode
    
#     def addChargingStation(self, chargingStation):
#         if chargingStation.pincode == self.pincode:
#             self.chargingStations.append(chargingStation)
#         else:
#             print("Charging Station does not belong to this area")

#     def getAvailableStations(self):
#         resultStations = []
#         for chargingStation in self.chargingStations:
#             if chargingStation.checkAvailability():
#                 resultStations.append(chargingStation)
#         return resultStations

from map_service import MapService
class Area:
    # postal_code
    # stations = []
    
    def __init__(self, postal_code):
        self.postal_code = postal_code
        self.stations = []

    def addChargingStation(self, chargingStation):
        if chargingStation.postal_code == self.postal_code:
            self.stations.append(chargingStation)

    def find_station_by_id(self, station_id):
        for station in self.stations:
            if station.station_id == station_id:
                return station
        return None