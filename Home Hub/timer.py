from machine import RTC

# Setup RTC
rtc = RTC()
rtc.datetime((1000, 1, 1, 0, 0, 0, 0, 0)) # Setting up RTC

class TIMER:
    def __init__(self, endTime):
        startTime = rtc.datetime()
        self.targetTime = self.addTime(endTime, startTime)
    
    def addTime(self, endTime, startTime):
        """
        year: 4-digit year (e.g., 2024)
        month: 1-12 (e.g., 3)
        day: 1-31 (e.g., 18)
        weekday: 0-6 (0 is Monday)
        hour: 0-23 (e.g., 14)
        minute: 0-59 (e.g., 31)
        second: 0-59 (e.g., 43)
        microsecond: 0-999999 (optional
        """
        convertedEndTime = self.convertToTime(endTime)
        finalEndTime = (0, 0, 0, 0, convertedEndTime[0], convertedEndTime[1], convertedEndTime[2], 0)
        result = (startTime[0] + convertedEndTime[0], startTime[1] + convertedEndTime[1], startTime[2] + convertedEndTime[2], startTime[3] + convertedEndTime[3], startTime[4] + convertedEndTime[4], startTime[5] + convertedEndTime[5], startTime[6] + convertedEndTime[6], startTime[7] + convertedEndTime[7])
        return result

    def convertToTime(self, secs):        
        if 3600 > secs >= 60:
            return (0, 0, 0, 0, 0, secs//60, secs%60, 0)
        elif secs >= 3600:
            return (0, 0, 0, 0, secs//3600, secs%3600, secs%60, 0)
        else:
            return (0, 0, 0, 0, 0, 0, secs, 0)

    def startTimer(self, endTime):
        startTime = rtc.datetime()
        self.targetTime = self.addTime(endTime, startTime)

    def checkTime(self):
        print(rtc.datetime(), self.targetTime)
        if rtc.datetime() >= self.targetTime:
            return True
        return False