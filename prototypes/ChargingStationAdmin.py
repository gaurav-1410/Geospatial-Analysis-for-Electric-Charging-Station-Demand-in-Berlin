class ChargingStationAdmin(User):
    ownedStations = []

    def __init__(self, id, userArea):
        super().__init__(id, userArea)
    
    def addChargingStation(self, station):
        ownedStations.append(station)
    
    def findStation(self, station_id):
        for station in ownedStations:
            if station.get_station_id() == station_id:
                return station
        return None