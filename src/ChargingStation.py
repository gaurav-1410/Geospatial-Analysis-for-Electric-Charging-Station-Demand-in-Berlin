# class ChargingStation:
#     station_id
#     street_address
#     available_plugs
#     total_plugs
#     demand
#     pincode
#     reports = []
#     feedbacks = []

#     def __init__(self, postal_code, station_id):
#         self.postal_code = postal_code
#         self.id = station_id
    
#     def get_station_id(self):
#         return self.station_id

#     def checkAvailability(self):
#         if available_plugs == 0:
#             return False
#         else:
#             return True
    
#     def ChargeYourVehicle(self):
#         if checkAvailability():
#             available_plugs -= 1
#             return True
#         else:
#             return False
    
#     def getDemand(self):
#         return demand

#     def addFeedback(self, feedback):
#         feedbacks.append(feedback)

#     def addReport(self, report):
#         reports.append(report)
    
class ChargingStation:
    # station_id
    # postal_code
    # latitude
    # longitude
    # feedbacks = []

    def __init__(self, station_id, postal_code, latitude, longitude):
        self.station_id = station_id
        self.postal_code = postal_code
        self.latitude = latitude
        self.longitude = longitude
        self.feedbacks = []
    
    def get_station_id(self):
        return self.station_id

    def addFeedback(self, feedback):
        self.feedbacks.append(feedback)