class Area:
    pincode
    chargingStations = []
    
    def __init__(self, pincode):
        self.pincode = pincode
    
    def addChargingStation(self, chargingStation):
        if chargingStation.pincode == self.pincode:
            self.chargingStations.append(chargingStation)
        else:
            print("Charging Station does not belong to this area")

    def getAvailableStations(self):
        resultStations = []
        for chargingStation in self.chargingStations:
            if chargingStation.checkAvailability():
                resultStations.append(chargingStation)
        return resultStations

    