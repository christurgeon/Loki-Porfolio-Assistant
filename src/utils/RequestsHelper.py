import requests



def getRequestWrapper(logging, url, params=None, msg=None, propagate=True, retries=3):
    headers = { "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36" }
    response = None
    for i in range(retries):
        try:
            response = requests.get(url=url, params=params, headers=headers)
            response.raise_for_status()
            break
        except Exception as e:
            logging.error(e)
            if msg:
                logging.error(msg)
            if i == retries - 1 and propagate:
                raise e 
    return response