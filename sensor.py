import time
import RPi.GPIO as GPIO
from time import sleep
from PowerWheelsCar import logger

Logger = logger
trigPin = 23
echoPin = 24
MAX_DISTANCE = 10000
timeOut=MAX_DISTANCE*60
GPIO.setmode(GPIO.BCM)
GPIO.setup(trigPin, GPIO.OUT) # set trigPin to output mode
GPIO.setup(echoPin, GPIO.IN)
""" This module detects objects using the ultrasonic and sends feedback to the main(radar) module"""
def pulseIn(pin,level,timeOut): # function pulseIn: obtain pulse time of a pin
    t0 = time.time()
    while(GPIO.input(pin) != level):
        if((time.time() - t0) > timeOut*0.000001):
            return 0;
    t0 = time.time()
    while(GPIO.input(pin) == level):
        if((time.time() - t0) > timeOut*0.000001):
            return 0;
    pulseTime = (time.time() - t0)*1000000
    return pulseTime

def getSonar(): #get the measurement results of ultrasonic module,with unit: cm
    GPIO.output(trigPin,GPIO.HIGH) #make trigPin send 10us high level
    sleep(0.00001) #10us
    GPIO.output(trigPin,GPIO.LOW)
    pingTime = pulseIn(echoPin,GPIO.HIGH,timeOut) #read plus time of echoPin
    distance = pingTime * 340.0 / 2.0 / 10000.0 # the sound speed is 340m/s, andcalculate distance (cm)
    return distance
    
def ultrasonicRead():
    Logger.info(getSonar())
    return getSonar()
