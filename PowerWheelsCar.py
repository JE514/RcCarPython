import bluetooth
import RPi.GPIO as GPIO
from time import sleep
import time
from rccarsensor import ultrasonicRead

enabled = True
trigPin = 23
echoPin = 24
MAX_DISTANCE = 10000
timeOut=MAX_DISTANCE*60
in1 = 14
ena = 18
temp1=1
buzzerPin=17
directionTicksPer = 1 #(Ticks of rotation)/100 #100 is for input value


GPIO.setmode(GPIO.BCM)
GPIO.setup(trigPin, GPIO.OUT) # set trigPin to output mode
GPIO.setup(echoPin, GPIO.IN)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(ena,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.setup(buzzerPin, GPIO.OUT)
GPIO.output(buzzerPin, GPIO.LOW)
motor=GPIO.PWM(ena,1000)

motor.start(25)
bd_addr = "DC:A6:32:6B:38:BD"
uuid = "42b58f76-b26d-11ea-b733-cb205305bc99"
port = 1

server_socket = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
server_socket.bind((bd_addr, bluetooth.PORT_ANY))
server_socket.listen(port)
print("Bluetooth Bind: listening on port " + str(port))
def enabledAlert(length, amount):
    buzz=amount
    while (buzz > 0):
        if buzz > 0:
            print("xd")
            GPIO.setmode(GPIO.BCM)
            GPIO.output(buzzerPin,GPIO.HIGH)
            sleep(length)
            GPIO.output(buzzerPin,GPIO.LOW)
            sleep(length)
            buzz = buzz-1
        else:
            break



#enabledAlert(0.1, 3)
bluetooth.advertise_service(server_socket, "SampleServer", service_classes=[bluetooth.SERIAL_PORT_CLASS],profiles=[bluetooth.SERIAL_PORT_PROFILE])
print("Bluetooth: Advertising service!")

client_socket, address = server_socket.accept()
print("Bluetooth: Accepting client!")
#server_socket.send('\x1a')
print("Bluetooth device Is connected!")
#enabledAlert(0.2, 2)


def return_data():
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print(data)
            return data
    except OSError:
        pass
print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
print("\n")
from threading import Thread
def sendCollisionWarning():
    while True:
        distance = ultrasonicRead()
        if distance < 10:
            print("Collison warning")
            client_socket.send("cw")
        
thread=Thread(target=sendCollisionWarning)
thread.start()

while(1):
    print('Loop')
    x=return_data()
    if x == None:
        print("disconnected")
        disconnected = True
        client_socket, address = server_socket.accept()
        if disconnected == True:
            print("Reconnected!")

    elif x==bytes('r', 'UTF-8'):
        print("run")
        if(temp1==1):
         GPIO.output(in1,GPIO.HIGH)
         GPIO.output(in2,GPIO.LOW)
         print("forward")
         x='z'
        else:
         GPIO.output(in1,GPIO.LOW)
         GPIO.output(in2,GPIO.HIGH)
         print("backward")
         x='z'

    elif bytes(':','UTF-8') in x:
        #MAIN DRIVE CODE.
        speed = x.decode('UTF-8').split(':')[1].replace("'",'')
        direction = x.decode('UTF-8').split(':')[3].replace("'",'')
        if enabled == True:
            #GPIO.output(in1,GPIO.HIGH) #high = forward?
            speed = float(speed)
            if speed > 0:
                GPIO.output(in1,GPIO.HIGH) #High = forwards ??????
                motor.ChangeDutyCycle(speed)
            elif speed < 0:
                GPIO.output(in1,GPIO.LOW) #Low = backwards ??????
                motor.ChangeDutyCycle(-speed)
            else:
                GPIO.output(in1,GPIO.LOW)
                motor.ChangeDutyCycle(0)
            if direction != 0:
                directionPosition = direction * directionTicksPer
                #Set servo To directionPosition
    elif x==bytes('s', 'UTF-8'):
        print("stop")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        enabled = False
        x='z'

    elif x==bytes('en', 'UTF-8'):
        print("Enable")
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
