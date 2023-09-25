import json
import requests  # type: ignore
from . import consts as c
from . import exceptions, utils
from app.core.config import settings


class Client(object):
    def __init__(self, use_server_time=False, flag="1"):
        print("CLINET API_KEY", settings.OKX_API_KEY)
        print("CLINET API_SECRET_KEY", settings.OKX_SECRET_KEY)
        print("CLINET PASSPHRASE", settings.OKX_PASSPHRASE)
        self.API_KEY = settings.OKX_API_KEY
        self.API_SECRET_KEY = settings.OKX_SECRET_KEY
        self.PASSPHRASE = settings.OKX_PASSPHRASE
        self.use_server_time = use_server_time
        self.flag = flag

    def _request(self, method, request_path, params):
        if method == c.GET:
            request_path = request_path + utils.parse_params_to_str(params)
        # url
        url = c.API_URL + request_path

        timestamp = utils.get_timestamp()

        # sign & header
        if self.use_server_time:
            timestamp = self._get_timestamp()

        body = json.dumps(params) if method == c.POST else ""

        sign = utils.sign(
            utils.pre_hash(timestamp, method, request_path, str(body)),
            self.API_SECRET_KEY,
        )
        header = utils.get_header(
            self.API_KEY, sign, timestamp, self.PASSPHRASE, self.flag
        )

        # send request
        response = None

        if method == c.GET:
            response = requests.get(url, headers=header)
        elif method == c.POST:
            response = requests.post(url, data=body, headers=header)

        # exception handle
        # print(response.headers)

        if not str(response.status_code).startswith("2"):
            raise exceptions.OkxAPIException(response)

        return response.json()

    def _request_without_params(self, method, request_path):
        return self._request(method, request_path, {})

    def _request_with_params(self, method, request_path, params):
        return self._request(method, request_path, params)

    def _get_timestamp(self):
        url = c.API_URL + c.SERVER_TIMESTAMP_URL
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()["data"][0]["ts"]
        else:
            return ""
