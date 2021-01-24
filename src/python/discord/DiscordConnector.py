if __name__ == "__main__" and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import config
import sys

def main():
    pass

if __name__ == "__main__":
    rc = -1
    try:
        rc = main()
    except Exception as e:
        logging.error("Exception: {}".format(e))
    logging.info("END rc = {}".foramt(tc))
    sys.exit(rc)
