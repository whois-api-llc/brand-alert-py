from requests import request, Response
from ..exceptions.error import ApiAuthError, HttpApiError, BadRequestError
from ..version import VERSION, LIBRARY_NAME
import logging


class ApiRequester:
    __logger = logging.getLogger("api-requester")
    __connect_timeout = 5
    __user_agent = "{name}/{ver}".format(name=LIBRARY_NAME, ver=VERSION)
    _base_url: str
    _timeout: float

    def __init__(self, **kwargs):
        """

        :param kwargs: Supported parameters:
        - base_url: (optional) API endpoint URL; str
        - timeout: (optional) API call timeout in seconds; float
        """
        self._base_url = ''
        self.timeout = 30

        if 'base_url' in kwargs:
            self.base_url = kwargs['base_url']
        if 'timeout' in kwargs:
            self.timeout = kwargs['timeout']

    @property
    def base_url(self) -> str:
        return self._base_url

    @base_url.setter
    def base_url(self, url: str):
        if url is None or len(url) <= 8 or not url.startswith('http'):
            raise ValueError("Invalid URL specified.")
        self._base_url = url

    @property
    def timeout(self) -> float:
        """API call timeout in seconds"""
        return self._timeout

    @timeout.setter
    def timeout(self, value: float):
        """API call timeout in seconds"""
        if value is not None and 1 <= value <= 60:
            self._timeout = value
        else:
            raise ValueError("Timeout value should be in [1, 60]")

    def get(self, payload: dict) -> str:
        headers = {
            'User-Agent': ApiRequester.__user_agent,
            'Connection': 'close'
        }
        response = request(
            "GET",
            self.base_url,
            params=payload,
            headers=headers,
            timeout=(ApiRequester.__connect_timeout, self.timeout)
        )

        return ApiRequester._handle_response(response)

    def post(self, data: dict) -> str:
        headers = {
            'User-Agent': ApiRequester.__user_agent,
            'Connection': 'close'
        }
        if 'apiKey' in data:
            headers['X-Authentication-Token'] = data.pop('apiKey')

        response = request(
            'POST',
            self.base_url,
            json=data,
            headers=headers,
            timeout=(ApiRequester.__connect_timeout, self.timeout)
        )

        return ApiRequester._handle_response(response)

    @staticmethod
    def _handle_response(response: Response) -> str:
        if 200 <= response.status_code < 300:
            return response.content.decode('UTF-8')

        if response.status_code in [401, 402, 403]:
            raise ApiAuthError(response.text)

        if response.status_code in [400, 422]:
            raise BadRequestError(response.text)

        if response.status_code >= 300:
            raise HttpApiError(response.text)
