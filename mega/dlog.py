
from django.conf import settings

import logging

def getlogger():
    logger = logging.getLogger()
    hdlr = logging.FileHandler(settings.LIST_VARS.get('log_file', ''))
    formatter = logging.Formatter('[%(asctime)s]%(levelname)-8s"%(message)s"','%Y-%m-%d %a %H:%M:%S') 
    
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.NOTSET)

    return logger

def debug(msg):
    logger = getlogger()
    logger.debug(msg)
    
LOGGER = getlogger()