import copy
import datetime
import re

from .base import BaseModel
import sys

if sys.version_info < (3, 9):
    import typing


_re_date_format = re.compile(r'^\d\d\d\d-\d\d-\d\d$')


def _date_value(values: dict, key: str) -> datetime.date or None:
    if key in values and values[key] is not None:
        if _re_date_format.match(values[key]) is not None:
            return datetime.datetime.strptime(
                values[key], '%Y-%m-%d').date()

    return None


def _string_value(values: dict, key: str) -> str:
    if key in values:
        return str(values[key])
    return ''


def _int_value(values: dict, key: str) -> int:
    if key in values:
        return int(values[key])
    return 0


def _list_value(values: dict, key: str) -> list:
    if key in values and type(values[key]) is list:
        return copy.deepcopy(values[key])
    return []


def _list_of_objects(values: dict, key: str, classname: str) -> list:
    r = []
    if key in values and type(values[key]) is list:
        r = [globals()[classname](x) for x in values[key]]
    return r


class Domain(BaseModel):
    domain_name: str
    action: str
    date: datetime.date or None

    def __init__(self, values):
        super().__init__()

        self.domain_name = ''
        self.action = ''
        self.date = None

        if values is not None:
            self.domain_name = _string_value(values, 'domainName')
            self.action = _string_value(values, 'action')
            self.date = _date_value(values, 'date')


class Response(BaseModel):
    domains_count: int
    if sys.version_info < (3, 9):
        domains_list: typing.List[Domain]
    else:
        domains_list: [Domain]

    def __init__(self, values):
        super().__init__()

        self.domains_count = 0
        self.domains_list = []

        if values is not None:
            self.domains_count = _int_value(values, 'domainsCount')
            self.domains_list = _list_of_objects(
                values, 'domainsList', 'Domain')


class ErrorMessage(BaseModel):
    code: int
    message: str

    def __init__(self, values):
        super().__init__()

        self.int = 0
        self.message = ''

        if values is not None:
            self.code = _int_value(values, 'code')
            self.message = _string_value(values, 'messages')
