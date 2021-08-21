if __name__ == "__main__" and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import os
import io
import config
import sys
import logging.handlers
import re
import requests
import pandas as pd
import LokiLogger 

LOGPATH      = config.logpath
MODULE_NAME  = "".join(c for c in os.path.splitext(os.path.basename(__file__))[0] if c.isalnum() or c == "_")
LOGFILE_NAME = "Log_{}.log".format(MODULE_NAME)
ARGUMENTS    = [r"top\s+\d+$", r"all$"] 
LOWFLOAT     = r"|".join([r"^low\s+{}".format(s) for s in ARGUMENTS]) 
HIGHFLOAT    = r"|".join([r"^high\s+{}".format(s) for s in ARGUMENTS])


# have options to search specific ticker for the data

class ShortInterestTracker: 

    def __init__(self): 
        self.lowfloat = re.compile(LOWFLOAT, re.IGNORECASE) 
        self.highfloat = re.compile(HIGHFLOAT, re.IGNORECASE)
        self.logging = LokiLogger.getLogger(__name__)

    def parseShortLevels(self, arg): 
        pass


