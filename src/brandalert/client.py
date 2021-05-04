import datetime
from json import loads, JSONDecodeError
import re

from .net.http import ApiRequester
from .models.response import Response
from .exceptions.error import ParameterError, EmptyApiKeyError, \
    UnparsableApiResponseError


class Client:
    __default_url = "https://brand-alert.whoisxmlapi.com/api/v2"
    _api_requester: ApiRequester or None
    _api_key: str

    _re_api_key = re.compile(r'^at_[a-z0-9]{29}$', re.IGNORECASE)
    _re_response_format = re.compile(r'^(json)|(xml)$', re.IGNORECASE)

    PREVIEW_MODE = 'preview'
    PURCHASE_MODE = 'purchase'
    _PARSABLE_FORMAT = 'json'

    JSON_FORMAT = 'JSON'
    XML_FORMAT = 'XML'

    def __init__(self, api_key: str, **kwargs):
        """
        :param api_key: str: Your API key.
        :key base_url: str: (optional) API endpoint URL.
        :key timeout: float: (optional) API call timeout in seconds
        """
        self._api_key = ''

        self.api_key = api_key

        if 'base_url' not in kwargs:
            kwargs['base_url'] = Client.__default_url

        self.api_requester = ApiRequester(**kwargs)

    @property
    def api_key(self) -> str:
        return self._api_key

    @api_key.setter
    def api_key(self, value: str):
        self._api_key = Client._validate_api_key(value)

    @property
    def api_requester(self) -> ApiRequester or None:
        return self._api_requester

    @api_requester.setter
    def api_requester(self, value: ApiRequester):
        self._api_requester = value

    @property
    def base_url(self) -> str:
        return self._api_requester.base_url

    @base_url.setter
    def base_url(self, value: str or None):
        if value is None:
            self._api_requester.base_url = Client.__default_url
        else:
            self._api_requester.base_url = value

    @property
    def timeout(self) -> float:
        return self._api_requester.timeout

    @timeout.setter
    def timeout(self, value: float):
        self._api_requester.timeout = value

    def preview(self, terms: list, **kwargs) -> Response:
        """
        Get the number of related domain names.

        :param list terms: (type: list of strings) search term list to be
                included in domain names.
        :key exclude_terms: (optional, type: list of strings) terms
                list not to be present in domain names
        :key since_date: (optional, type: datetime.date) Domain's changes in
                the response are not older than this date (default: yesterday)
        :key with_typos: (optional, type: bool) Enrich search terms with
                possible typos (default: False)
        :key punycode: (optional, type: bool) Return domains in punycode
                (default: True)
        :return: `Response` instance
        :raises ConnectionError:
        :raises BrandAlertApiError: Base class for all errors below
        :raises EmptyApiKeyError:
        :raises ResponseError: response contains an error message
        :raises ApiAuthError: Server returned 401, 402 or 403 HTTP code
        :raises BadRequestError: Server returned 400 or 422 HTTP code
        :raises HttpApiError: HTTP code >= 300 and not equal to above codes
        :raises UnparsableApiResponseError: the response couldn't be parsed
        :raises ParameterError: invalid parameter's value
        """

        kwargs['mode'] = Client.PREVIEW_MODE
        return self.data(terms, **kwargs)

    def purchase(self, terms: list, **kwargs) -> Response:
        """
        Get domains list.

        :param list terms: (type: list of strings) search term list to be
                included in domain names.
        :key exclude_terms: (optional, type: list of strings) terms
                list not to be present in domain names
        :key since_date: (optional, type: datetime.date) Domain's changes in
                the response are not older than this date (default: yesterday)
        :key with_typos: (optional, type: bool) Enrich search terms with
                possible typos (default: False)
        :key punycode: (optional, type: bool) Return domains in punycode
                (default: True)
        :return: `Response` instance
        :raises ConnectionError:
        :raises BrandAlertApiError: Base class for all errors below
        :raises EmptyApiKeyError:
        :raises ResponseError: response contains an error message
        :raises ApiAuthError: Server returned 401, 402 or 403 HTTP code
        :raises BadRequestError: Server returned 400 or 422 HTTP code
        :raises HttpApiError: HTTP code >= 300 and not equal to above codes
        :raises UnparsableApiResponseError: the response couldn't be parsed
        :raises ParameterError: invalid parameter's value
        """

        kwargs['mode'] = Client.PURCHASE_MODE
        return self.data(terms, **kwargs)

    def data(self, terms: list, **kwargs) -> Response:
        """
        Get parsed API response as a `Response` instance.

        :param list terms: (type: list of strings) search terms list to be
                included in domain names.
        :key exclude_terms: (optional, type: list of strings) terms
                list not to be present in domain names
        :key since_date: (optional, type: datetime.date) Domain's changes in
                the response are not older than this date (default: yesterday)
        :key with_typos: (optional, type: bool) Enrich search terms with
                possible typos (default: False)
        :key punycode: (optional, type: bool) Return domains in punycode
                (default: True)
        :key mode: (optional, default: preview) use `PREVIEW_MODE` and
                `PURCHASE_MODE` constants
        :return: `Response` instance
        :raises ConnectionError:
        :raises BrandAlertApiError: Base class for all errors below
        :raises ResponseError: response contains an error message
        :raises ApiAuthError: Server returned 401, 402 or 403 HTTP code
        :raises BadRequestError: Server returned 400 or 422 HTTP code
        :raises HttpApiError: HTTP code >= 300 and not equal to above codes
        :raises ParameterError: invalid parameter's value
        """
        kwargs['response_format'] = Client._PARSABLE_FORMAT

        response = self.raw_data(terms, **kwargs)
        try:
            parsed = loads(str(response))
            if 'domainsCount' in parsed:
                return Response(parsed)
            raise UnparsableApiResponseError(
                "Could not find the correct root element.", None)
        except JSONDecodeError as error:
            raise UnparsableApiResponseError("Could not parse API response", error)

    def raw_data(self, terms: list, **kwargs) -> str:
        """
        Get raw API response.

        :param list terms: (type: list of strings) search terms list to be
                included in domain names.
        :key exclude_terms: (optional, type: list of strings) terms
                list not to be present in domain names
        :key since_date: (optional, type: datetime.date) Domain's changes in
                the response are not older than this date (default: yesterday)
        :key with_typos: (optional, type: bool) Enrich search terms with
                possible typos (default: False)
        :key punycode: (optional, type: bool) Return domains in punycode
                (default: True)
        :key response_format: (optional, type: str) use constants
                JSON_FORMAT and XML_FORMAT
        :key mode: (optional, default: preview) use `PREVIEW_MODE` and
                `PURCHASE_MODE` constants
        :return: str
        :raises ConnectionError:
        :raises BrandAlertApiError: Base class for all errors below
        :raises ResponseError: response contains an error message
        :raises ApiAuthError: Server returned 401, 402 or 403 HTTP code
        :raises BadRequestError: Server returned 400 or 422 HTTP code
        :raises HttpApiError: HTTP code >= 300 and not equal to above codes
        :raises ParameterError: invalid parameter's value
        """
        if self.api_key == '':
            raise EmptyApiKeyError('')

        include_terms = Client._validate_terms(terms, True)
        if 'exclude_terms' in kwargs:
            exclude_terms = Client._validate_terms(kwargs['exclude_terms'])
        else:
            exclude_terms = []

        if 'response_format' in kwargs:
            response_format = Client._validate_response_format(
                kwargs['response_format'])
        else:
            response_format = Client._PARSABLE_FORMAT

        if 'mode' in kwargs:
            mode = Client._validate_mode(kwargs['mode'])
        else:
            mode = Client.PREVIEW_MODE

        if 'since_date' in kwargs:
            since_date = Client._validate_since_date(kwargs['since_date'])
        else:
            today = datetime.date.today()
            since_date = datetime.date(today.year, today.month, today.day - 1)

        if 'with_typos' in kwargs:
            with_typos = Client._validate_bool_value(kwargs['with_typos'])
        else:
            with_typos = False

        if 'punycode' in kwargs:
            punycode = Client._validate_bool_value(kwargs['punycode'])
        else:
            punycode = True

        return self._api_requester.post(self._build_payload(
            include_terms,
            exclude_terms,
            mode,
            since_date,
            with_typos,
            punycode,
            response_format
        ))

    @staticmethod
    def _validate_api_key(api_key) -> str:
        if Client._re_api_key.search(
                str(api_key)
        ) is not None:
            return str(api_key)
        else:
            raise ParameterError("Invalid API key format.")

    @staticmethod
    def _validate_mode(value: str) -> str:
        if value.lower() not in [Client.PREVIEW_MODE, Client.PURCHASE_MODE]:
            raise ParameterError('Incorrect value.')
        return value.lower()

    @staticmethod
    def _validate_terms(values: list, required=False) -> list:
        if type(values) is not list:
            raise ParameterError('Parameter should be a list')
        filtered = list(
            filter(lambda x: x is not None and len(str(x)) > 0, values))

        if len(filtered) <= 0 and required:
            raise ParameterError('No valid terms in a list')
        filtered = [str(x) for x in filtered]
        return filtered

    @staticmethod
    def _validate_since_date(value: datetime.date) -> datetime.date:
        if value is not None and isinstance(value, datetime.date):
            delta = datetime.date.today() - value
            if 0 <= delta.days <= 14:
                return value
        raise ParameterError('Incorrect since_date value.')

    @staticmethod
    def _validate_response_format(_format):
        if Client._re_response_format.search(str(_format)) is not None:
            return str(_format)
        else:
            raise ParameterError(
                "Output format should be either JSON or XML.")

    @staticmethod
    def _validate_bool_value(value: bool) -> bool:
        if value is not None and type(value) is bool:
            return value
        raise ParameterError('The value should be True or False.')

    def _build_payload(self, include_terms, exclude_terms, mode,
                       since_date, with_typos, punycode, response_format):
        return {
            'apiKey': self.api_key,
            'includeSearchTerms': include_terms,
            'excludeSearchTerms': exclude_terms,
            'mode': mode,
            'sinceDate': str(since_date),
            'withTypos': with_typos,
            'punycode': punycode,
            'responseFormat': response_format
        }
