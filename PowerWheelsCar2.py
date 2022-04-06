import bluetooth
import RPi.GPIO as GPIO
from time import sleep
import time
import os 
from sensor import ultrasonicRead
from Logger import Logger
#from rccarsensor import ultrasonicRead


enabled = True
in1 = 14
ena = 10 #18
servoPin = 17
temp1=1
buzzerPin=17
directionTicksPer = 1 #(Ticks of rotation)/100 #100 is for input value
os.system ("sudo pigpiod")
time.sleep(1)
import pigpio 
logger = Logger("robotLog")

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(ena,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.setup(buzzerPin, GPIO.OUT)
GPIO.output(buzzerPin, GPIO.LOW)
GPIO.setup(servoPin, GPIO.OUT)
motor=GPIO.PWM(ena,50)
steerServo = GPIO.PWM(servoPin, 50) # GPIO 17 for PWM with 50Hz
steerServo.start(2.5)
motor.start(25)
bd_addr = "B8:27:EB:D6:57:CE" #DC:A6:32:6B:38:BD
uuid = "42b58f76-b26d-11ea-b733-cb205305bc99"
port = 1

ESC = 4
pi = pigpio.pi();
pi.set_servo_pulsewidth(ESC, 0)

server_socket = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
server_socket.bind((bd_addr, bluetooth.PORT_ANY))
server_socket.listen(port)
logger.info("Bluetooth Bind: Listening on port " + str(port))
#print("Bluetooth Bind: listening on port " + str(port))
def enabledAlert(length, amount):
    buzz=amount
    while (buzz > 0):
        if buzz > 0:
            logger.info("Buzzer Alert")
            #print("xd")
            GPIO.setmode(GPIO.BCM)
            GPIO.output(buzzerPin,GPIO.HIGH)
            sleep(length)
            GPIO.output(buzzerPin,GPIO.LOW)
            sleep(length)
            buzz = buzz-1
        else:
            break
            
def log(message):
    logger.info(message)
    
def arm(): #This is the arming procedure of an ESC 
    print("Connect the battery and press Enter")
    inp = input()
    if inp == "":
        print("arm")
        pi.set_servo_pulsewidth(ESC, 0)
        time.sleep(1)
        pi.set_servo_pulsewidth(ESC, 2000)
        time.sleep(1)
        pi.set_servo_pulsewidth(ESC, 1500)

#enabledAlert(0.1, 3)
bluetooth.advertise_service(server_socket, "SampleServer", service_classes=[bluetooth.SERIAL_PORT_CLASS],profiles=[bluetooth.SERIAL_PORT_PROFILE])
logger.info("Bluetooth: Advertising Service!")
#print("Bluetooth: Advertising service!")]


client_socket, address = server_socket.accept()
logger.info("Bluetooth: Accepting client!")
#print("Bluetooth: Accepting client!")
#server_socket.send('\x1a')
logger.info("Bluetooth: Device connected!")
#print("Bluetooth device Is connected!")
#enabledAlert(0.2, 2)


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
#print("\n")
#print("Robot Program Started...")
#print("\n")
logger.info("\n")
logger.info("Robot Program Started...")
logger.info("\n")
arm()
from threading import Thread
def sendCollisionWarning():
    while True:
        distance = ultrasonicRead()
        if distance < 10:
            logger.info("Collision warning")
            #print("Collison warning")
            client_socket.send("cw")
        
thread=Thread(target=sendCollisionWarning)
thread.start()

while(1):
    logger.info("Loop")
    #print('Loop')
    x=return_data()
    if x == None:
        logger.info("Bluetooth: disconnected!")
        #print("disconnected")
        disconnected = True
        client_socket, address = server_socket.accept()
        if disconnected == True:
            logger.info("Bluetooth: Reconnected!")
            #print("Reconnected!")

    elif x==bytes('r', 'UTF-8'):
        logger.info("run")
        #print("run")
        if(temp1==1):
         GPIO.output(in1,GPIO.HIGH)
         logger.info("forward")
         #print("forward")
         x='z'
        else:
         GPIO.output(in1,GPIO.LOW)
         logger.info("backward")
         #print("backward")
         x='z'

    elif bytes(':','UTF-8') in x:
        #MAIN DRIVE CODE.
        speed = x.decode('UTF-8').split(':')[1].replace("'",'')
        direction = x.decode('UTF-8').split(':')[3].replace("'",'')
        if enabled == True:
            #GPIO.output(in1,GPIO.HIGH) #high = forward?
            speed = float(speed)
            if speed > 0:#0
                GPIO.output(in1,GPIO.HIGH) #High = forwards ??????
                #motor.ChangeDutyCycle(speed)
                pi.set_servo_pulsewidth(ESC, speed*5+1500)
            elif speed < 0: #0
                GPIO.output(in1,GPIO.LOW) #Low = backwards ??????
                #motor.ChangeDutyCycle(-speed)
                pi.set_servo_pulsewidth(ESC, 1500 - speed * 5)
            else:
                GPIO.output(in1,GPIO.LOW)
                #motor.ChangeDutyCycle(0)
            if direction != 0:
                directionPosition = direction * directionTicksPer
                #Set servo To directionPosition
    elif x==bytes('s', 'UTF-8'):
        logger.info("Stopping robot...")
        #print("stop")
        GPIO.output(in1,GPIO.LOW)
        pi.set_servo_pulsewidth(ESC, 0)
        enabled = False
        x='z'

    elif x==bytes('en', 'UTF-8'):
        logger.info("Robot Enabled")
        #print("Enable")
        enabled = True
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
    else:
        client_socket.send("<<<  wrong data  >>>")
        client_socket.send("please enter the defined data to continue.....")

