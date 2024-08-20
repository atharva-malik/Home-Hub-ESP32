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
from machine import Pin, ADC, PWM
import time

# OLED Import
from oled import *

# Temp import and setup
from dht import DHT22
tempSensor = DHT22(42)

# Buzzer import and setup
import buzzerPy

# Slider setup
p4 = Pin(4, Pin.IN)
sl = ADC(p4)
sl.atten(ADC.ATTN_11DB) # This is to make it work with the 3.3v power supply
sliderVal = sl.read() # Ranges from 0-4095 (inclusive)

# Led Bar Graph setup
barGraphPins = [Pin(46, Pin.OUT), Pin(3, Pin.OUT), Pin(8, Pin.OUT), Pin(18, Pin.OUT), Pin(17, Pin.OUT), Pin(16, Pin.OUT), Pin(15, Pin.OUT), Pin(7, Pin.OUT), Pin(6, Pin.OUT), Pin(5, Pin.OUT)]

# Buzzer setup
buzzer = buzzerPy.BUZZER(Pin(9, Pin.OUT))

# Planning out the variables:
isSessOn = False
cTemp = 80 # Current Temperature
cHum = 80 # Current Humidity
timeLeft = 0 # Time Left in Session
targetTime = 0
sesLen = 0 # Session length
sliderVal = 0
warning = False
err = None
btnPressTime = 750

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
    

def updateGraph(target, current, temp=0):
    val = mapValue(current, temp, target, 0, 10)
    valToGraph(val)


# Update Functions
def checkTemps(currentTemperature, currentHumidity):
    global warning
    global btnPressTime
    global err
    feelsLikeTemperature = (currentTemperature * 0.7) + (currentHumidity * 0.3)
    if not warning and btnPressTime > 750:
        if feelsLikeTemperature > 36:
            err = "TH"
        elif feelsLikeTemperature < 10:
            err = "TC"
        else:
            err = None
            buzzer.notone()
    else:
        if feelsLikeTemperature < 36 and feelsLikeTemperature > 10 and err != "S":
            buzzer.notone()
            warning = False
            err = None
    if err == "TH":
        warning = True
        buzzer.tone(buzzerPy.A5)
    elif err == "TC":
        warning = True
        buzzer.tone(buzzerPy.A5)

def checkButton():
    global warning
    global btnPressTime
    global err
    global isSessOn
    global targetTime
    if warning and readButton(10) and err != "S":
        warning = False
        err = None
        btnPressTime = 0
        buzzer.notone()
    elif warning and readButton(10) and err == "S":
        targetTime = 0
        isSessOn = False
        warning = False
        err = None
        btnPressTime = 0
    elif not isSessOn and readButton(10) and sl.read() > 0:
        isSessOn = True
        targetTime = mapValue(sl.read(), 0, 4095, 0, 60)

def checkSession():
    global isSessOn
    if isSessOn:
        time.sleep(1)
        timeLeft -= 1
        if timeLeft <= 0:
            timeLeft = 0
            targetTime = 0
            isSessOn = False
            buzzer.tone(buzzerPy.A5)
            warning = True
            err = "S"

def checkSlider():
    global sliderVal
    global targetTime
    slVal = sl.read()
    sliderVal = mapValue(slVal, 0, 4095, 0, 10)
    if sliderVal != 0 and isSessOn != True:
        valToGraph(sliderVal)

def updateScreen():
    global targetTime
    temp, hum = getTemp()
    flt = (temp * 0.7) + (hum * 0.3)
    displayText(("Temperature: " + str(round(flt)) + "c"), 0, 0)
    displayText(("Humidity: " + str(hum) + "%"), 0, 10, False)
    if isSessOn:
        displayText(("Time left: " + str(timeLeft) + "m"), 0, 30, False)
        updateGraph(targetTime, timeLeft)
    elif sl.read() > 0:
        displayText(("Target Time: " + str(targetTime) + "m"), 0, 30, False)
        displayText("Press button to", 0, 40, False)
        displayText("start the session", -5, 50, False)
    else:
        updateGraph(86, flt, 5)


cTemp, cHum = getTemp()
while True:
    cTemp, cHum = getTemp()
    checkTemps(cTemp, cHum)
    checkButton()
    checkSlider() # This is only in case the session is over
    updateScreen()
    checkSession()
    # print(btnPressTime)
    print(targetTime, sl.read(), mapValue(sl.read(), 0, 4095, 0, 60))
    btnPressTime += 1 # AROUND 10 ish FPS
    targetTime = mapValue(sl.read(), 0, 4095, 0, 60)
