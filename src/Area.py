class Area:

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