if __name__ == "__main__" and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import os
import config
import logging.handlers

LOGPATH = config.logpath
MODULE_NAME = "".join(c for c in os.path.splitext(os.path.basename(__file__))[0] if c.isalnum() or c == "_")
LOGFILE_NAME = "Log_{}.log".format(MODULE_NAME)

def main():
    return 0

if __name__ == "__main__":
    log_file_name = os.path.join(LOGPATH, LOGFILE_NAME)
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)-8s %(message)s",
                        datefmt="%m-%d %H:%M:%S")
    handler = logging.handlers.TimedRotatingFileHandler(log_file_name, when="d", interval=1, backupCount=5)
    formatter = logging.Formatter("%(asctime)s[%(levelname)-8s]%(message)s")
    handler.setFormatter(formatter)
    logging.getLogger("").addHandler(handler)
    logging.info("========================================")
    logging.info("START")
    rc = -1
    try:
        rc = main()
    except Exception as e:
        logging.error("Exception: {}".format(e))
    logging.info("END rc = {}".format(rc))
    sys.exit(rc)
