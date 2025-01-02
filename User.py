class User:
    id
    userArea = None
    feedbacks = []
    reports = []

    def __init__(self, id,userArea):
        self.id = id
        self.userArea = userArea
    
    def getAvailableStation(self, area):
        return area.getAvailableStations()
    
    def giveFeedback(self, chargingStation):
        feedback = Feedback()
        feedback.setChargingStationId(chargingStation.get_station_id())

        while True:
            rating = int(input("Enter your rating from 1 to 5: "))
            if rating < 1 or rating > 5:
                print("Rating should be between 1 and 5")
            else:
                feedback.setRating(rating)
                break

        while True:
            answer = input(print("Do you want to add a comment? (Y/N)"))
            if answer == 'Y':
                feedback.setComment(input("Enter your comment: "))
                break
            elif answer == 'N':
                break
            else:
                print("Invalid input")
        chargingStation.addFeedback(feedback)
        feedbacks.append(feedback)
    


    def writeReport(self, chargingStation):
        report = Report()
        report.chargingStationId = chargingStation.get_station_id()
        report.setReportComment(input("Enter your report: "))
        chargingStation.addReport(report)
        reports.append(report)