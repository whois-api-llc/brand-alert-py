.. image:: https://img.shields.io/badge/License-MIT-green.svg
    :alt: brand-alert-py license
    :target: https://opensource.org/licenses/MIT

.. image:: https://img.shields.io/pypi/v/brand-alert.svg
    :alt: brand-alert-py release
    :target: https://pypi.org/project/brand-alert

.. image:: https://github.com/whois-api-llc/brand-alert-py/workflows/Build/badge.svg
    :alt: brand-alert-py build
    :target: https://github.com/whois-api-llc/brand-alert-py/actions

========
Overview
========

The client library for
`Brand Alert API <https://brand-alert.whoisxmlapi.com/>`_
in Python language.

The minimum Python version is 3.6.

Installation
============

.. code-block:: shell

    pip install brand-alert

Examples
========

Full API documentation available `here <https://brand-alert.whoisxmlapi.com/api/documentation/making-requests>`_

Create a new client
-------------------

.. code-block:: python

    from brandalert import *

    client = Client('Your API key')

Make basic requests
-------------------

.. code-block:: python

    # Get the number of domains.
    result = client.preview(['google'])
    print(result.domains_count)

    # Get raw API response
    raw_result = client.raw_data(
        ['google'],
        response_format=Client.XML_FORMAT,
        mode=Client.PREVIEW_MODE)

    # Get list of recently registered/dropped domains (up to 10,000)
    result = client.purchase(['google'])

Advanced usage
-------------------

Extra request parameters

.. code-block:: python

    today = datetime.date.today()
    delta = datetime.timedelta(days=10)
    result = client.purchase(
        ['google'],
        exclude_terms=['blog'],
        since_date=today - delta,
        with_typos=True,
        punycode=False)

    raw_result = client.raw_data(
        ['google'],
        exclude_terms=['blog'],
        since_date=today - delta,
        with_typos=True,
        punycode=False,
        mode=Client.PURCHASE_MODE,
        response_format=Client.JSON_FORMAT)
