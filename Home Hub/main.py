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
from machine import Pin, ADC
import time

# Slider setup
p4 = Pin(4, Pin.IN)
sl = ADC(p4)
sl.atten(ADC.ATTN_11DB) # This is to make it work with the 3.3v power supply
sliderVal = sl.read() # Ranges from 0-4095 (inclusive)

# Led Bar Graph setup
barGraphPins = [Pin(46, Pin.OUT), Pin(3, Pin.OUT), Pin(8, Pin.OUT), Pin(18, Pin.OUT), Pin(17, Pin.OUT), Pin(16, Pin.OUT), Pin(15, Pin.OUT), Pin(7, Pin.OUT), Pin(6, Pin.OUT), Pin(5, Pin.OUT)]

# Planning out the variables:
cTemp = 0 # Current Temperature
cHum = 0 # Current Humidity
timeLeft = 0 # Time Left in Session
sesLen = 0 # Session length

# Generic functions
def mapValue(value, range1_min, range1_max, range2_min, range2_max):
    ratio = (value - range1_min) / (range1_max - range1_min)
    mapped_value = ratio * (range2_max - range2_min) + range2_min
    return int(mapped_value)

# Bar Graph functions
def valToGraph(value):
    for i in range(10):
        if i < value:
            barGraphPins[i].value(1)
        else:
            barGraphPins[i].value(0)

while True:
  sliderVal = mapValue(sl.read(), 0, 4095, 0, 10)
  valToGraph(sliderVal)
