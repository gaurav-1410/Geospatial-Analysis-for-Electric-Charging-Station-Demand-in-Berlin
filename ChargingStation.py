class ChargingStation:
    station_id
    street_address
    available_plugs
    total_plugs
    demand
    pincode
    reports = []
    feedbacks = []

    def __init__(self, station_id, street_address, total_plugs, demand, pincode):
        self.station_id = station_id
        self.street_address = street_address
        self.available_plugs = total_plugs
        self.total_plugs = total_plugs
        self.demand = demand
        self.pincode = pincode
    
    def get_station_id(self):
        return self.station_id

    def checkAvailability(self):
        if available_plugs == 0:
            return False
        else:
            return True
    
    def ChargeYourVehicle(self):
        if checkAvailability():
            available_plugs -= 1
            return True
        else:
            return False
    
    def getDemand(self):
        return demand
        
    def addReport(self):
        report = input("Enter your report: ")
        reports.append(report)

    def addFeedback(self, feedback):
        feedbacks.append(feedback)

    def addReport(self, report):
        reports.append(report)
    