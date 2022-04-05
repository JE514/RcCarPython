
def logger(msg):
  print(msg)
  #log to file
  #log to controller console
  
def logger(msg, var):
  data = msg.replace("{}", var)
  print(data)
  #log to file
  #log to controller console
