import logging

def Logger(): 
  logger = logging.getLogger('robotLog')
  logger.setLevel(logging.DEBUG)
  # create file handler which logs even debug messages
  fh = logging.FileHandler('robotLog.log')
  fh.setLevel(logging.INFO)
  logger.addHandler(fh)
  return logger.getLogger()

