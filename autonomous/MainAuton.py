import PowerWheels
from sensor import ultrasonicRead
#import pigpio #MIGHT NEED
pi, ESC, servo = PowerWheels.getDrive()
logger = PowerWheels.getLogger()
motorNeutralSpeed, directionTicksPer, enabled, motorMinSpeed, motorMaxSpeed, autonMode = PowerWheels.getConstants()
sock, disconnected = PowerWheels.getSocket()
autonEnabled = False
distance = 0.0
driveSpeed = 0.0

def driveMotor(speedPercent):
  speed = 0.0
  if speedPercent > 0:
    speed = motorNeutralSpeed+speedPercent*5
  else:
    speed = speedPercent*5+motorNeutralSpeed
  driveSpeed = speed
  pi.set_servo_pulsewidth(ESC, speed)
  
def getDriveSpeed():
  return driveSpeed

def getAutonEnabled():
  return autonEnabled


def enableAuton(enabled, mode=0):
  if getAutonEnabled() == True and enabled == True:
    logger.info("Auton: Already Enabled")
  elif getAutonEnabled() == False and enabled == False:
    logger.info("Auton: Already Disabled")
  elif enabled == True:
    if autonMode != 0:
      autonMode = mode
      PowerWheels.setAutonMode(mode)
    logger.info("Auton: Enabling Auton In Mode " + autonMode)
  else:
    logger.info("Auton: Disabling Auton")

  
while PowerWheels.getAutonEnabled():
  logger.info("Auton: Autonomous Mode Active.")
  distance = ultrasonicRead()
  
  if autonMode == 1: #simple auton mode 
    if getDriveSpeed() != 20.0:
      driveMotor(20.0)
    if distance < 10:
      logger.info("Auton: Distance within 10, Stopping Robot...")
      driveMotor(0.0)
    

