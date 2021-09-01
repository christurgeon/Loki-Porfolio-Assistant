import os
import logging 
import config

class Logger:
    
    def getLogger(name):
        log_format = '%(asctime)s  %(name)8s  %(levelname)5s  %(message)s'
        logging.basicConfig(level=logging.INFO,
                            format=log_format,
                            filename=os.path.join(config.logpath, 'dev.log'),
                            filemode='w')
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(logging.Formatter(log_format))
        logging.getLogger(name).addHandler(console)
        return logging.getLogger(name)