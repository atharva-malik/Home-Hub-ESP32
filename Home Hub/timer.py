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
        result = (0, 0, 0, 0, 0, 0, 0, 0)
        for i, t in enumerate(startTime):
            result[i] = t+

    def convertToTime(self, secs):        
        if 3600 > secs >= 60:
            return (0, secs//60, secs%60)
        elif secs >= 3600:
            return (secs//3600, secs%3600, secs%60)
        else:
            return (0, 0, secs)

    def startTimer(self, endTime):
        startTime = rtc.datetime()
        self.targetTime = self.addTime(endTime, startTime)

    def checkTime(self):
        print(rtc.datetime(), self.targetTime)
        if rtc.datetime() >= self.targetTime:
            return True
        return False