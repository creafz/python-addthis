==============
python-addthis
==============

A Python wrapper for the `AddThis Analytics API <http://support.addthis.com/customer/portal/articles/381264-addthis-analytics-api/>`_.

Requirements
------------
* Python 2.6, 2.7 or 3.2+
* `python-requests <https://pypi.python.org/pypi/requests/>`_ library.

Installation
------------
Install from PyPI::

    pip install python-addthis

Usage
-----

::

    from addthis import Addthis

    # create an AddThis instance using userid and password from your AddThis account and optionally provide a pubid.
    addthis = Addthis(userid="YOUR_USER_ID", password="YOUR_PASSWORD", pubid="YOUR_PUB_ID")

    # get the number of shares for the last day
    print addthis.shares.day()

    # get the number of shares by day for the last week
    print addthis.shares.day(period="week")


You can see a full documentation for supported metrics and dimensions at http://support.addthis.com/customer/portal/articles/381264-addthis-analytics-api

A few more examples
~~~~~~~~~~~~~~~~~~~

**How many times was my content shared on Twitter, by day, over the last week?**
::

    >>> addthis.shares.day(period="week", service="twitter")

**What were my top shared urls for the pubid="MY_PUB_ID"?**
::

    >>> addthis.shares.url(pubid="MY_PUB_ID")

**How many users shared my content this month, broken down by their interests?**
::

    >>> addthis.sharers.interest(period="month")

**Which sharing services sent the most clicks back to my site this week?**
::

    >>> addthis.clicks.service(period="week")

Exceptions
----------

AddthisValidationError
~~~~~~~~~~~~~~~~~~~~~~
Addthis object expects to be called with 2 parameters - "metric" and "dimension"::

    addthis.<metric>.<dimension>()


For example::

     >>> addthis.shares.day() # "shares" is a metric and "day" is a dimension.


If it gets another number of parameters (e.g. addthis.shares() or addthis.shares.day.week()) it will raise an **AddthisValidationError**.

AddthisError
~~~~~~~~~~~~
**AddthisError** is raised when AddThis service returns a response with a HTTP status code other than 200. The exception object has 4 attributes:

* *status_code*: Code from the HTTP response.
* *code*, *message*, *attachment*: Error attributes from the AddThis response body. (see the “Error" section in the `AddThis Analytics API documentation <http://support.addthis.com/customer/portal/articles/381264-addthis-analytics-api/>`_ for more information).