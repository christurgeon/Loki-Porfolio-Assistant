if __name__ == "__main__" and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


import config
import sys
import requests
from itertools import islice  
from bs4 import BeautifulSoup
from utils.LokiLogger import Logger


MAX_ENTRIES = 25


class ShortInterest: 

    def __init__(self): 
        self.lowfloat_url = config.lowfloat
        self.highfloat_url = config.highfloat
        self.logging = Logger.getLogger(__name__)

    def fetchRangeShortInterest(self, num_entries=MAX_ENTRIES, lowfloat=True): 
        url = self.lowfloat_url if lowfloat else self.highfloat_url
        num_entries = MAX_ENTRIES if num_entries <= 0 else min(MAX_ENTRIES, num_entries)
        try:
            response = requests.get(url=self.lowfloat_url)
            response.raise_for_status()
            html = BeautifulSoup(response.content, "html.parser")
            table = html.find("table", {"class" : "stocks"})
            count = 0
            result = ["<table>"]
            for idx, row in enumerate(islice(table, 1, len(table))):
                if str(row) == "\n":
                    continue
                if count == num_entries + 1:
                    break
                result.append(str(row))
                count += 1
                print(count)
            result.append("</table>")
            return (''.join(result), count)
        except Exception as e:
            self.logging.exception(f"Failed to fetch lowfloat: {e}")


if __name__ == "__main__":
    s = ShortInterest()
    ###################
    # TEST
    ###################