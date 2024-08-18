from machine import RTC

# Setup RTC
rtc = RTC()
rtc.datetime((1000, 1, 1, 0, 0, 0, 0, 0)) # Setting up RTC

class TIMER:
    def __init__(self, end_time):
        self.startTime = rtc.datetime()
    
    def getTime(self):
        print(type(self.startTime))
        print(rtc.datetime - self.startTime)