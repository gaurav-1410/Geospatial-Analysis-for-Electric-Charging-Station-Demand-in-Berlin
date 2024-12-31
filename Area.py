class Area:
    pincode
    ChargingStation[] chargingStations
    def __init__(self, pincode):
        self.pincode = pincode
        self.chargingStations = []
    
    def addChargingStation(self, chargingStation):
        if chargingStation.pincode == self.pincode:
            self.chargingStations.append(chargingStation)
        else
            print("Charging Station does not belong to this area")

    def findAvailableChargingStation(self):
        resultStations = []
        for chargingStation in self.chargingStations:
            if chargingStation.checkAvailability():
                resultStations.append(chargingStation)
        return resultStations

    