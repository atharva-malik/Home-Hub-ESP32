# Requirements:
# Time my sessions
# Warn me if something's amiss (i.e.: Too hot/Too cold/Too humid/Too long spent sitting)
# Set new timers
# View current stats (Temp/Humidity/Time Left)

# Parts List:
# ESP32-s3: https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/_images/ESP32-S3_DevKitC-1_pinlayout_v1.1.jpg
# Bar Graph: (Session Time/Temp/Humidity)
# Rotating thing: To switch the bar graph around
# Sliding thing: To set session time
# Temp/Humidity Sensor
# Buzzer: To tell me if smth is wrong
# Button: To reset session

# Generic Imports
from machine import Pin, ADC, PWM, RTC, Timer
import time, timer

# OLED Import
from oled import *

# Temp import and setup
from dht import DHT22
tempSensor = DHT22(42)

# Buzzer import and setup
from buzzerPy import BUZZER, mario, jingle, twinkle

# Slider setup
p4 = Pin(4, Pin.IN)
sl = ADC(p4)
sl.atten(ADC.ATTN_11DB) # This is to make it work with the 3.3v power supply
sliderVal = sl.read() # Ranges from 0-4095 (inclusive)

# Led Bar Graph setup
barGraphPins = [Pin(46, Pin.OUT), Pin(3, Pin.OUT), Pin(8, Pin.OUT), Pin(18, Pin.OUT), Pin(17, Pin.OUT), Pin(16, Pin.OUT), Pin(15, Pin.OUT), Pin(7, Pin.OUT), Pin(6, Pin.OUT), Pin(5, Pin.OUT)]

# Buzzer setup
buzzer = BUZZER(Pin(9, Pin.OUT))

# Planning out the variables:
cTemp = 0 # Current Temperature
cHum = 0 # Current Humidity
timeLeft = 0 # Time Left in Session
sesLen = 0 # Session length

# Setup RTC
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
rtc = RTC()
rtc.datetime((1000, 1, 1, 0, 0, 0, 0, 0)) # Setting up RTC
"""
LOTS OF RESEARCH

This is for future reference
start_time = rtc.datetime()
# Perform actions...
end_time = rtc.datetime()
elapsed_time = end_time - start_time

# Create a timer that fires every 5 seconds
timer = Timer(-1)
timer.init(period=5, mode=Timer.PERIODIC, callback=callbackFunction)

Timer Parameters
period: The time interval between timer events, in seconds.
mode: The timer mode:
machine.Timer.ONE_SHOT: The timer fires once and then stops.
machine.Timer.PERIODIC: The timer fires repeatedly at the specified interval.
callback: A function to be called when the timer fires.

timer.deinit() # This stops the timer
"""

# Generic functions
def mapValue(value, range1_min, range1_max, range2_min, range2_max):
    ratio = (value - range1_min) / (range1_max - range1_min)
    mapped_value = ratio * (range2_max - range2_min) + range2_min
    return int(mapped_value)

def getTemp():
    try:
        tempSensor.measure()
        temp = tempSensor.temperature()
        humidity = tempSensor.humidity()
    except Exception as e:
        print(e)
        temp, humidity = -1, -1
    return temp, humidity

def callbackFunction(timer):
    print("Time UP!")

def readButton(pinNum):
    pin = Pin(pinNum, Pin.IN)
    return pin.value()

# Bar Graph functions
def valToGraph(value):
    for i in range(10):
        if i < value:
            barGraphPins[i].value(1)
        else:
            barGraphPins[i].value(0)
    
    # sliderVal = mapValue(sl.read(), 0, 4095, 0, 10)
    # valToGraph(sliderVal)


time = timer.TIMER(12)
displayImage(EYES, 64, 64)
time.startTimer(12)
while True:
    print(getTemp())
    print(readButton(10))
    print(time.checkTime())