import requests
import logging
from common import log_config
import datetime


def execute_http(url, method="GET", data=None, params=None, headers={'Content-Type': 'application/json'}, timeout=10, cookies={}, verify=False):
    if "eureka" not in url and "api-docs" not in url:
        logging.info("start to execute http request with url: {}, method: {}, data: {}, headers: {}".format(url, method, data, headers))
        logging.info("http execution starts at {}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %f')))
    if method == "GET":
        res = requests.get(url, data=data, params=params, headers=headers, timeout=timeout, cookies=cookies, verify=verify)
    elif method == "POST":
        res = requests.post(url, data=data, params=params, headers=headers, timeout=timeout, cookies=cookies, verify=verify)
    elif method == "HEAD":
        res = requests.post(url, data=data, params=params, headers=headers, timeout=timeout, cookies=cookies, verify=verify)
    elif method == "OPTIONS":
        res = requests.options(url, data=data, params=params, headers=headers, timeout=timeout, cookies=cookies, verify=verify)
    elif method == "PUT":
        res = requests.put(url, data=data, params=params, headers=headers, timeout=timeout, cookies=cookies, verify=verify)
    elif method == "PATCH":
        res = requests.patch(url, data=data, params=params, headers=headers, timeout=timeout, cookies=cookies, verify=verify)
    elif method == "DELETE":
        res = requests.delete(url, data=data, params=params, headers=headers, timeout=timeout, cookies=cookies, verify=verify)
    if "eureka" not in url and "api-docs" not in url:
        logging.info("http execution ends at {}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %f')))
        logging.info("http execute cost time {}".format(res.elapsed))
        logging.info("http execute response: {}".format(res.text))
        logging.info("http execute response cookies: {}".format(res.cookies))
        logging.info("http execute response headers: {}".format(res.headers))
    return res.text, res.status_code, res.cookies.get_dict(), res.headers


