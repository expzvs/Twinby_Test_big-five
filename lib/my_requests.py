import requests
import json
from lib.logger import Logger
import allure
from enviroment import ENV_OBJECT

class MyRequests():

    @staticmethod
    def post(url: str, data: dict = None, headers: dict= None, cookies: dict = None):
        with allure.step(f"POST request to URL '{url}"):
            return MyRequests._send(url, data, headers, cookies, 'POST')

    @staticmethod
    def post_j(url: str, data: dict = None, headers: dict= None, cookies: dict = None):
        with allure.step(f"POST request to URL '{url} fro JSON"):
            if headers is None:
                headers = {"Content-Type": "application/json"}
            return MyRequests._send(url, json.dumps(data), headers, cookies, 'POST')

    @staticmethod
    def get(url: str, data: dict = None, headers: dict= None, cookies: dict = None):
        with allure.step(f"GET request to URL '{url}"):
            return MyRequests._send(url, data, headers, cookies, 'GET')

    @staticmethod
    def _send(url: str, data: dict, headers: dict, cookies: dict, method: str):

        url = f"{ENV_OBJECT.get_base_url()}{url}"

        if headers is None:
            headers = {}
        if cookies is None:
            cookies = {}

        Logger.add_request(url, data, headers, cookies, method)

        if method == 'GET':
            res = requests.get(url, params=data, headers=headers, cookies=cookies)
        elif method == 'POST':
            res = requests.post(url, data=data, headers=headers, cookies=cookies)
        else:
            raise Exception(f"Bad HTTP method '{method}' was received")

        Logger.add_response(res)

        return res
