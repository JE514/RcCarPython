import pygame
import bluetooth
from Logger import Logger
import sys
from time import sleep

#0 = SQUARE
#1 = X
#2 = CIRCLE
#3 = TRIANGLE
#4 = L1
#5 = R1
#6 = L2
#7 = R2
#8 = SHARE
#9 = OPTIONS
#10 = LEFT ANALOG PRESS
#11 = RIGHT ANALOG PRESS
#12 = PS4 ON BUTTON
#13 = TOUCHPAD PRESS

def return_data():
    try:
        while True:
            data = sock.recv(1024)
            if not data:
                break
            print(data)
            return data
    except OSError:
        pass
bluetoothAddress = "DC:A6:32:6B:38:BD"  #"B8:27:EB:D6:57:CE"  
#B8:27:EB:6B:AB:4B
stickDeadband = 2

logger = Logger("clientLog")
sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )

sock.connect((bluetoothAddress, 1));
sock.setblocking(False)
pygame.init()
j = pygame.joystick.Joystick(0)
j.init()
def enableRobot():
    sock.send("en")
    logger.info("Controller: Sending Enable Request!")
def enableAutonMode():
    logger.info("Controler: Enabled Autonomous Mode!")
def disableAutonMode():
    logger.info("Controler: Disabled Autonomous Mode!")
    
def stopRobot():
    sock.send("s")
    
def squareDown():
    sock.send("ho")
    
def squareUp():
    sock.send("ho")
 
#enableRobot()

def loop():
    sleep(0.02) #sleep 20 ms
    try:
        speed = float(round(j.get_axis(1) * -100))
        direction = float(round(j.get_axis(3) * 100)) #axis 0
        if direction < stickDeadband and direction > -stickDeadband:
            direction = 0.0
        if speed > -101 and direction > -101:
            logger.info("PRE: M:" + str(speed) + ":D:" + str(direction))
            sock.send(":M:" + str(speed) + ":D:" + str(direction))
    except:
        logger.warn("EXCEPTION: LOOP FUNCTION INFO: sysinfo: " + str(sys.exc_info()[0]) + " speed: " + str(speed) + " direction: " + str(direction))
    
    
while True:
    try:
        loop()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.JOYBUTTONDOWN:
                if j.get_button(0): #square
                    squareDown()
                if j.get_button(1): #X
                     enableRobot()
                if j.get_button(2): #circle
                    enableAutonMode()
                if j.get_button(3): #triangle
                    disableAutonMode()
            elif event.type == pygame.JOYBUTTONUP:
                if j.get_button(0): #square
                    squareUp()
                
        x=return_data()
        if x is not None:
            if bytes(':','UTF-8') in x:
                xd = x.decode('UTF-8').split(":")[1]
                print("Collision warning " + xd + " cm")
            else:
                data = return_data().replace("b'", "").replace("'","")
                logger.info(data)
              
  
               
    except KeyboardInterrupt:
        stopRobot()
        print("EXITING NOW")
        j.quit()
        x.toString()
