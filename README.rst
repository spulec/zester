Zester
=========================

Zester is a library that makes it easier to develop Python clients for websites without APIs.

No lxml, no XPath, just javascript.

Let's make a client library for `Hacker News <http://news.ycombinator.com/>`_ by saving the following code in a file named hnclient.py::

    from zester import MultipleClient, Attribute

    class HNClient(MultipleClient):
        url = "http://news.ycombinator.com/"
        title = Attribute(selector="$('.title a')", modifier="$(el).html()")
        link = Attribute(selector="$('.title a')"), modifier="$(el).attr('href')")
        points = Attribute(selector="$('.subtext span')", modifier="$(el).html().replace(' points', '')")

Now, let's use the client we just made. Open a python shell::

    >>> from hnclient import HNClient
    >>> client = HNClient()
    >>> stories = client.process()
    >>> stories[0]
    HNClientResponse(points=u'200', link=u'http://daltoncaldwell.com/what-twitter-could-have-been', title=u'What Twitter could have been')
    >>> print stories[0].title
    What Twitter could have been
    >>> print stories[0].link
    http://daltoncaldwell.com/what-twitter-could-have-been
    >>> print stories[0].points
    56

We subclassed MultipleClient there because we were planning on returning multiple results. If we wanted to make a client for something like `Weather.gov <http://weather.gov>`_ that returned a single result, we could do something like this::

    from zester import SingleClient, Attribute

    class WeatherClient(SingleClient):
        url = "http://forecast.weather.gov/MapClick.php?lat={lat}&lon={lng}"
        temperature = Attribute(selector="$('.myforecast-current-lrg').html()")
        humidity = Attribute(selector="$('.current-conditions-detail li').contents()[1]")
        heat_index = Attribute(selector="$('.current-conditions-detail li').contents()[11]")

        def __init__(self, lat, lng, *args, **kwargs):
            super(WeatherClient, self).__init__(*args, **kwargs)
            self.url = self.url.format(lat=lat, lng=lng)

This also demonstrates how you can allow arguments to be taken::

    >>> from weather_client import WeatherClient
    >>> client = WeatherClient(lat=40.7143528, lng=-74.0059731)
    >>> curr_weather = client.process()
    >>> curr_weather
    WeatherClientResponse(heat_index=u'82\xb0F (28\xb0C)', temperature=u'80\xb0F', humidity=u'58%')
    >>> print curr_weather.temperature
    80°F
    >>> print curr_weather.humidity
    58%
    >>> print curr_weather.heat_index
    82°F (28°C)


Installation
------------

To install zester, simply: ::

    $ pip install zester
