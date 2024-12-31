class User:
    id
    Area UserArea
    Feedback[] feedbacks

    def __init__(self, id,userArea):
        self.id = id
        self.userArea = userArea
    
    def getAvailableStation(self):
        return self.userArea.getAvailableStations()
    
