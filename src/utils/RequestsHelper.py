import requests


def getRequestWrapper(logging, url, params=None, msg=None, propagate=True, retries=3):
    response = None
    for i in range(retries):
        try:
            response = requests.get(url=url, params=params)
            response.raise_for_status()
            break
        except Exception as e:
            logging.error(e)
            if msg:
                logging.error(msg)
            if i == retries - 1 and propagate:
                raise e 
    return response