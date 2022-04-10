import sys
#sys.path.append('/Desktop/RcCarProject')
from sensor import ultrasonicRead
#import pigpio #MIGHT NEED
autonEnabled = False
distance = 0.0
driveSpeed = 0.0

 
def setConstants(pi2,ESC2,servo2,logger2,motorNeutralSpeed2,directionTicksPer2,motorMinSpeed2,motorMaxSpeed2,autonMode2,sock2,disconnected2,isRobotEnabled2, autonEnabled2):
  pi = pi2
  ESC = ESC2
  servo = servo2
  logger = logger2
  motorNeutralSpeed = motorNeutralSpeed2
  directionTicksPer = directionTicksPer2
  motorMinSpeed = motorMinSpeed2
  autonMode = autonMode2
  sock = sock2
  disconnected = disconnected2
  isRobotEnabled = isRobotEnabled2
  autonEnabled = autonEnabled2
  
def updateVariables(sock2, disconnected2, isRobotEnabled2, autonEnabled2):
  sock = sock2
  disconnected = disconnected2
  isRobotEnabled = isRobotEnabled2
  autonEnabled = autonEnabled2

def getVariables():
  return autonMode
  

def driveMotor(speedPercent):
  speed = 0.0
  if speedPercent > 0:
    speed = motorNeutralSpeed+speedPercent*5
  else:
    speed = speedPercent*5+motorNeutralSpeed
  driveSpeed = speed
  pi.set_servo_pulsewidth(ESC, speed)

def steerServo(steerPercent):
  steer = 0.0
  if steerPercent > 0:
    steer = 2.0 #TEMP
  else:
    steer = 1.0 #TEMP
  
def getDriveSpeed():
  return driveSpeed

def getAutonEnabled():
  return autonEnabled


def enableAuton(enabled, mode=0):
  if getAutonEnabled() == True and enabled == True:
    logger.info("Auton: Already Enabled.")
    sock.send("Auton: Already Enabled.")
  elif getAutonEnabled() == False and enabled == False:
    logger.info("Auton: Already Disabled.")
    sock.send("Auton: Already Disabled.")
  elif enabled == True:
    if mode != 0:
      autonMode = mode
      getAutonMode(mode)
      #setAutonMode(mode)
    logger.info("Auton: Enabling Autonomous In Mode " + autonMode)
    sock.send("Auton: Enabling Autonomous In Mode " + autonMode)
  else:
    logger.info("Auton: Disabling Autonomous...")
    sock.send("Auton: Disabling Autonomous...")

  
while autonEnabled:
  distance = ultrasonicRead()
  if disconnected == False and isRobotEnabled == True:#isRobotEnabled() == True:
    
    if autonMode == 1: #simple auton mode 
      if getDriveSpeed() != 20.0:
        driveMotor(20.0)
      if distance < 10:
        logger.info("Auton: Distance within 10, Stopping Robot...")
        driveMotor(0.0)
    if autonMode == 2: #simple(But Fast) auton mode 
      if getDriveSpeed() != 50.0:
        driveMotor(50.0)
      if distance < 10:
        logger.info("Auton: Distance within 10, Stopping Robot...")
        driveMotor(0.0)
