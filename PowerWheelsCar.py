import bluetooth
import RPi.GPIO as GPIO
from time import sleep
import time
import os 
from sensor import ultrasonicRead
from Logger import Logger
import pigpio 

autonMode = 1
motorNeutralSpeed = 1500
motorMinSpeed = 1000
motorMaxSpeed = 2000
enabled = False
autonEnabled = False
ultrasonicSensorEnabled = False
servoPin = 18
ESC = 4
temp1=1
buzzerPin=17
directionTicksPer = 1 #(Ticks of rotation)/100 #100 is for input value
os.system ("sudo pigpiod")
time.sleep(1)
logger = Logger("robotLog")

GPIO.setmode(GPIO.BCM)
GPIO.setup(buzzerPin, GPIO.OUT)
GPIO.output(buzzerPin, GPIO.LOW)
bd_addr = "DC:A6:32:6B:38:BD"  #"B8:27:EB:D6:57:CE" 
uuid = "42b58f76-b26d-11ea-b733-cb205305bc99"
port = 1

pi = pigpio.pi();
pi.set_servo_pulsewidth(ESC, 0)

server_socket = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
server_socket.bind((bd_addr, bluetooth.PORT_ANY))
server_socket.listen(port)
logger.info("Bluetooth Bind: Listening on port " + str(port))
def enabledAlert(length, amount):
    buzz=amount
    while (buzz > 0):
        if buzz > 0:
            logger.info("Buzzer Alert")
            GPIO.setmode(GPIO.BCM)
            GPIO.output(buzzerPin,GPIO.HIGH)
            sleep(length)
            GPIO.output(buzzerPin,GPIO.LOW)
            sleep(length)
            buzz = buzz-1
        else:
            break
            
    
def arm(): #This is the arming procedure of an ESC 
    logger.info("ESC: ARMING ESC")
    pi.set_servo_pulsewidth(ESC, 0)
    time.sleep(1)
    pi.set_servo_pulsewidth(ESC, 2000)
    time.sleep(1)
    pi.set_servo_pulsewidth(ESC, 1500)
    logger.info("ESC: ESC ARMED")

#enabledAlert(0.1, 3)
bluetooth.advertise_service(server_socket, "SampleServer", service_classes=[bluetooth.SERIAL_PORT_CLASS],profiles=[bluetooth.SERIAL_PORT_PROFILE])
logger.info("Bluetooth: Advertising Service!")


client_socket, address = server_socket.accept()
logger.info("Bluetooth: Accepting client!")
#server_socket.send('\x1a')
logger.info("Bluetooth: Device connected!")
#enabledAlert(0.2, 2) #2 bluetooth connected 


    
def enableRobot():
    #arm() #TRYING WITHOUT ARMING SEQUENCE
    #enabledAlert(0.5, 3) #3 long enable robot
    enabled = True
    logger.info("Robot: Robot Enabled")
    
def getDrive():
    return [pi, ESC, servoPin]
    
def getLogger():
    return logger

def getAutonEnabled():
    return autonEnabled

def getConstants():
    return [motorNeutralSpeed,directionTicksPer,enabled,motorMinSpeed,motorMaxSpeed,autonMode]


    
def return_data():
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print(data) #PRINT LINEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
            return data
    except OSError:
        pass
    
logger.info("\n")
logger.info("Robot Program Started...")
logger.info("\n")

from threading import Thread
def sendCollisionWarning():
    while ultrasonicSensorEnabled == True:
        distance = ultrasonicRead()
        if distance < 10:
            logger.info("Collision warning")
            client_socket.send("cw")
        
thread=Thread(target=sendCollisionWarning)
thread.start()

while(1):
    x=return_data()
    if x == None:
        logger.info("Bluetooth: disconnected!")
        pi.set_servo_pulsewidth(ESC, 0)
        disconnected = True
        client_socket, address = server_socket.accept()
        if disconnected == True:
            logger.info("Bluetooth: Reconnected!")

    elif x==bytes('r', 'UTF-8'):
        if enabled == True:
            logger.info("run")
            if(temp1==1):
                pi.set_servo_pulsewidth(ESC, 2000)
                logger.info("forward")
                x='z'
            else:
                pi.set_servo_pulsewidth(ESC, 1000)
                logger.info("backward")
                x='z'

    elif bytes(':','UTF-8') in x:
        #MAIN DRIVE CODE.
        speed = x.decode('UTF-8').split(':')[2].replace("'",'')
        direction = x.decode('UTF-8').split(':')[4].replace("'",'')
        if enabled == True:
            try:
                speed = float(speed)
                direction = float(direction)
            except:
                speed = 0.0
                direction = 0.0
                logger.warn("Exception: speed or direction not a number")
            if speed > 0:#0
                pi.set_servo_pulsewidth(ESC, speed*5+motorNeutralSpeed)
            elif speed < 0: #0
                pi.set_servo_pulsewidth(ESC, motorNeutralSpeed + speed * 5)
            else:
                pi.set_servo_pulsewidth(ESC, 0)
            if direction < 0:
                directionPosition = -direction * directionTicksPer * 9.36 + 1489 # TEMP  
            else:
                directionPosition = 1489 - direction * directionTicksPer * 9.36#1489 mid servo position
            pi.set_servo_pulsewidth(servoPin, directionPosition)
                #Set servo To directionPosition
                
    elif x==bytes('s', 'UTF-8'):
        logger.info("Stopping robot...")
        pi.set_servo_pulsewidth(ESC, 0)
        enabled = False
        x='z'

    elif x==bytes('en', 'UTF-8'):
        logger.info("Robot Enabled")
        enabled = True
        enableRobot()
        x='z'

    elif x==bytes('e', 'UTF-8'):
        GPIO.cleanup()
        break
    elif x==bytes('ho','UTF-8'):
        if buzzer == False:
            GPIO.output(buzzerPin,GPIO.HIGH)
            buzzer = True
        elif buzzer == True:
            GPIO.output(buzzerPin,GPIO.LOW)
            buzzer = False
    elif x==bytes('au','UTF-8'):
        #Auton Mode
        autonEnabled = True
    else:
        client_socket.send("<<<  wrong data  >>>")
        client_socket.send("please enter the defined data to continue.....")

