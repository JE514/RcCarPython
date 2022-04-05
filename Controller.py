import pygame
import bluetooth


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
bluetoothAddress = "DC:A6:32:6B:38:BD"
stickDeadband = 0.2


sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )

sock.connect((bluetoothAddress, 1));
sock.setblocking(False)
pygame.init()
j = pygame.joystick.Joystick(0)
j.init()
def enableRobot():
    sock.send("en")
    
def stopRobot():
    sock.send("s")
    
def squareDown():
    sock.send("ho")
    
def squareUp():
    sock.send("ho")
 
enableRobot()
        
while True:
    try:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.JOYBUTTONDOWN:
                if j.get_button(0):
                    squareDown()
            elif event.type == pygame.JOYBUTTONUP:
                if j.get_button(0):
                    squareUp()
            if event.type == pygame.JOYAXISMOTION:
                speed = round(j.get_axis(1) * -100)
                direction = round(j.get_axis(3), 2) #axis 0
                if direction > stickDeadband:
                    #RIGHT
                    direction = direction * 100
                elif direction < -stickDeadband:
                    #LEFT
                    direction = direction * 100
                else:
                    direction = 0
                print("M:" + str(speed) + ":D:" + str(direction))
                sock.send("M:" + str(speed) + ":D:" + str(direction))
                 #if M: is Positive, go forward, If M is negative, go backwards
                 #If D: is positive Go Right, D: is negative go Left
        x=return_data()
        if x is not None:
            if bytes(':','UTF-8') in x:
                xd = x.decode('UTF-8').split(":")[1]
                print("Collision warning " + xd + " cm")
              
  
               
    except KeyboardInterrupt:
        stopRobot()
        print("EXITING NOW")
        j.quit()
        x.toString()
