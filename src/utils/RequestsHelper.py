import json
import requests
from itertools import cycle


PROXIES = None


def configureProxies():
    global PROXIES
    url = "https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list"
    try:
        print("HERE")
        response = requests.get(url)
        proxy_list_string = response.text.splitlines()
        if len(proxy_list_string) == 0:
            return
    except Exception as e:
        print(f"init_proxy_pool() failed: {e}")
        return
    proxies = set()
    for proxy in proxy_list_string:
        try:
            proxy = json.loads(proxy)
            if proxy["anonymity"] != "transparent":
                ip, port = proxy["export_address"][0], proxy["port"]
                proxies.add(f"{ip}:{port}")
        except:
            continue
    PROXIES = cycle(proxies)
    print(PROXIES)


def getRequestWrapper(logging, url, params=None, msg=None, propagate=True, retries=3):
    global PROXIES
    proxy = next(PROXIES) if PROXIES else None
    print(proxy) ########################################################
    headers = { "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36" }
    response = None
    for i in range(retries):
        try:
            proxy = { "http" : proxy, "https" : proxy }
            response = requests.get(url=url, params=params, headers=headers, proxies=proxy)
            response.raise_for_status()
            break
        except Exception as e:
            logging.error(e)
            if msg:
                logging.error(msg)
            if i == retries - 1 and propagate:
                raise e 
    return response