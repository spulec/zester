Zester
=========================

**This project is currently under development**

Zester is a library that makes it easier to develop Python clients for websites without APIs.

No lxml, no XPath, just javascript.

Let's make a client library for `Hacker News <http://news.ycombinator.com/>`_ by saving the following code in a file named hnclient.py::

    from zester import ClientLibrary, Attribute

    class HNClient(ClientLibrary):
        title = Attribute(selector="$('.title a')", modifier="$(el).html()")
        link = Attribute(selector="$('.title a')"), modifier="$(el).attr('href')")
        points = Attribute(selector="$('.subtext span')", modifier="$(el).html().replace(' points', '')")

        def __init__(self, url="http://news.ycombinator.com/"):
            self.url = url
            super(HNClient, self).__init__()


Now, let's use the client we just made. Open a python shell::

    >>> from hnclient import HNClient
    >>> client = HNClient()
    >>> stories = client.process()
    >>> print stories[0].title
    "What Twitter could have been"
    >>> print stories[0].link
    "http://daltoncaldwell.com/what-twitter-could-have-been"
    >>> print stories[0].points
    "56"
