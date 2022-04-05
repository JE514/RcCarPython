import sys
import logging
import logging.config

#def Logger(): 
  #logger = logging.getLogger('robotLog')
  #logger.setLevel(logging.DEBUG)
  # create file handler which logs even debug messages
  #fh = logging.FileHandler('robotLog.log')
  #logger.addHandler(fh)
  #return logger.getLogger()

def Logger(file_name):
        formatter = logging.Formatter(fmt='%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s',
                                      datefmt='%Y/%m/%d %H:%M:%S') # %I:%M:%S %p AM|PM format
        logging.basicConfig(filename = '%s.log' %(file_name),format= '%(asctime)s %(module)s,line: %(lineno)d %(levelname)8s | %(message)s',
                                      datefmt='%Y/%m/%d %H:%M:%S', filemode = 'w', level = logging.INFO)
        log_obj = logging.getLogger()
        log_obj.setLevel(logging.DEBUG)
        # log_obj = logging.getLogger().addHandler(logging.StreamHandler())

        # console printer
        screen_handler = logging.StreamHandler(stream=sys.stdout) #stream=sys.stdout is similar to normal print
        screen_handler.setFormatter(formatter)
        logging.getLogger().addHandler(screen_handler)
        
        fh = logging.FileHandler('robotLog.log')
        logging.getLogger().addHandler(fh)

        log_obj.info("Logger object created successfully..")
        return log_obj
