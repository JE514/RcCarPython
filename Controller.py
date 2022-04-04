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

sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )

sock.connect(("DC:A6:32:6B:38:BD", 1));
sock.setblocking(False)
pygame.init()

j = pygame.joystick.Joystick(0)
j.init()
while True:
    try:
        events = pygame.event.get()
        for event in events:
            #if event.type == pygame.JOYBUTTONDOWN:
                #sock.send("ho")
            #elif event.type == pygame.JOYBUTTONUP:
               # sock.send("ho2")
            if event.type == pygame.JOYAXISMOTION:
                Moutput = j.get_axis(1) * -100
                direction = j.get_axis(3)
                if direction > 0.2:
                    direction2 = "R"
                elif direction < -0.2:
                    direction2 = "L"
                else:
                    direction2 = "N"
                if Moutput < 0:
                    if direction > 0:
                        direction = direction * 100
                    else:
                        direction = direction * -100
                    sock.send(str(round(- Moutput)) + ":b:" + direction2 + ":" + str(direction))
                else:
                    if direction > 0:
                        direction = direction * 100
                    else:
                        direction = direction * -100
                    sock.send(str(round(Moutput)) + ":f:" + direction2 + ":" + str(direction))
        x=return_data()
        if x is not None:
            if bytes(':','UTF-8') in x:
                xd = x.decode('UTF-8').split(":")[1]
                print("Collision warning " + xd + " cm")

    except KeyboardInterrupt:
        print("EXITING NOW")
        j.quit()
        x.toString()
