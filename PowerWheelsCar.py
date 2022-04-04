import bluetooth
import RPi.GPIO as GPIO
from time import sleep
import time
from rccarsensor import ultrasonicRead
trigPin = 23
echoPin = 24
MAX_DISTANCE = 10000
timeOut=MAX_DISTANCE*60
in1 = 14
ena = 18
temp1=1
GPIO.setmode(GPIO.BCM)
GPIO.setup(trigPin, GPIO.OUT) # set trigPin to output mode
GPIO.setup(echoPin, GPIO.IN)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(ena,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
buzzerPin=17
GPIO.setup(buzzerPin, GPIO.OUT)
GPIO.output(buzzerPin, GPIO.LOW)
motor=GPIO.PWM(ena,1000)

motor.start(25)
bd_addr = "DC:A6:32:6B:38:BD"
uuid = "42b58f76-b26d-11ea-b733-cb205305bc99"
port = 1
server_socket = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
server_socket.bind((bd_addr, bluetooth.PORT_ANY))
server_socket.listen(1)
print("Bluetooth device Is connsected!1")
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
print("Bluetooth device Is connected!2")

client_socket, address = server_socket.accept()
print("Bluetooth device Is connected!3")
#server_socket.send('\x1a')
print("Bluetooth device Is connected!4")
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
        print("xd")
        cmd = x.decode('UTF-8').split(':')[1].replace("'",'')
        speed = x.decode('UTF-8').split(':')[0].replace("'",'')
        direction = x.decode('UTF-8').split(':')[2].replace("'",'')
        sspeed = x.decode('UTF-8').split(':')[3].replace("'",'')
        if cmd=="f":
            #r.ChangeDutyCycle(float(speed))
            #l.ChangeDutyCycle(float(speed))
            print("f")
            if float(speed) == 0.0:
                if direction != "N":
                  GPIO.output(in1,GPIO.HIGH)
                  motor.ChangeDutyCycle(float(sspeed))
                else:
                    motor.ChangeDutyCycle(0)
            else:
                GPIO.output(in1,GPIO.HIGH)
                if direction != "N":
                    if direction == "L":
                        l.ChangeDutyCycle(float(speed))
                        test = float(sspeed) / 10
                        thrustperc = (float(sspeed)) / 100
                        SLtrackspd = float(thrustperc) * float(speed)
                        #print(thrustperc + "XDD: " + str(SLtrackspd))
                        r.ChangeDutyCycle(test)
                        # r.ChangeDutyCycle(float(speed) - 10.0)
                        #l.ChangeDutyCycle(float(speed))
                    elif direction == "R":
                        r.ChangeDutyCycle(float(speed))
                        test = float(sspeed) / 10
                        thrustperc = (float(sspeed) - 10) / 100
                        SLtrackspd = float(thrustperc) * float(speed)
                        #print(thrustperc + "XDD: " + str(SLtrackspd))
                        l.ChangeDutyCycle(test)
                else:
                    r.ChangeDutyCycle(float(speed))
                    l.ChangeDutyCycle(float(speed))
        elif cmd=="b":
            GPIO.output(in1,GPIO.LOW)
            GPIO.output(in2,GPIO.HIGH)
            GPIO.output(in3,GPIO.LOW)
            GPIO.output(in4,GPIO.HIGH)
            #l.ChangeDutyCycle(float(speed))
            #r.ChangeDutyCycle(float(speed))
            if direction != "N":
                if direction == "L":
                    l.ChangeDutyCycle(float(speed))
                    test = float(sspeed) / 10
                    thrustperc = (float(sspeed)) / 100
                    SLtrackspd = float(thrustperc) * float(speed)
                    #print(thrustperc + "XDD: " + str(SLtrackspd))
                    r.ChangeDutyCycle(test)
                    # r.ChangeDutyCycle(float(speed) - 10.0)
                    #l.ChangeDutyCycle(float(speed))
                elif direction == "R":
                    r.ChangeDutyCycle(float(speed))
                    test2 = float(sspeed) / 10
                    thrustperc = (float(sspeed) - 10) / 100
                    SLtrackspd = float(thrustperc) * float(speed)
                    #print(thrustperc + "XDD: " + str(SLtrackspd))
                    l.ChangeDutyCycle(test2)
            else:
                r.ChangeDutyCycle(float(speed))
                l.ChangeDutyCycle(float(speed))

    elif x==bytes('s', 'UTF-8'):
        print("stop")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        x='z'

    elif x==bytes('f', 'UTF-8'):
        print("forward")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        temp1=1
        x='z'

    elif x==bytes('b', 'UTF-8'):
        print("backward")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        temp1=0
        x='z'

    elif x==bytes('l', 'UTF-8'):
        print("low")
        r.ChangeDutyCycle(25)
        x='z'

    elif x==bytes('m', 'UTF-8'):
        print("medium")
        r.ChangeDutyCycle(50)
        x='z'

    elif x==bytes('h', 'UTF-8'):
        print("high")
        l.ChangeDutyCycle(100)
        x='z'


    elif x==bytes('e', 'UTF-8'):
        GPIO.cleanup()
        break
    elif x==bytes('ho','UTF-8'):
        GPIO.output(buzzerPin,GPIO.HIGH)
    elif x==bytes('ho2','UTF-8'):
        GPIO.output(buzzerPin,GPIO.LOW)
    else:
        client_socket.send("<<<  wrong data  >>>")
        client_socket.send("please enter the defined data to continue.....")
