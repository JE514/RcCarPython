import PowerWheels
from sensor import ultrasonicRead
pi, ESC, servo = PowerWheels.getDrive()
logger = PowerWheels.getLogger()
motorNeutralSpeed, directionTicksPer, enabled, motorMinSpeed, motorMaxSpeed, autonMode = PowerWheels.getConstants()
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

  
while PowerWheels.getAutonEnabled():
  logger.info("Auton: Autonomous Mode Active.")
  distance = ultrasonicRead()
  
  if autonMode == 1: #simple auton mode 
    if getDriveSpeed() != 20.0:
      driveMotor(20.0)
    if distance < 10:
      logger.info("Auton: Distance within 10, Stopping Robot...")
      driveMotor(0.0)
    

