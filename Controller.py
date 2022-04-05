import pygame
import bluetooth

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
while True:
    try:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.JOYBUTTONDOWN:
                sock.send("ho")
            elif event.type == pygame.JOYBUTTONUP:
               sock.send("ho")
            if event.type == pygame.JOYAXISMOTION:
                speed = round(j.get_axis(1), 1) * -100
                direction = round(j.get_axis(3), 1)
                if direction > stickDeadband:
                    #RIGHT
                    direction = direction * 100
                elif direction < -stickDeadband:
                    #LEFT
                    direction = direction * -100
                else:
                    return
                print("M:" + str(-speed) + ":D:" + str(direction))
                sock.send("M:" + str(-speed) + ":D:" + str(direction))
                 #if M: is Positive, go forward, If M is negative, go backwards
                    #If D: is positive Go Right, D: is negative go Left
        x=return_data()
        if x is not None:
            if bytes(':','UTF-8') in x:
                xd = x.decode('UTF-8').split(":")[1]
                print("Collision warning " + xd + " cm")

    except KeyboardInterrupt:
        print("EXITING NOW")
        j.quit()
        x.toString()
