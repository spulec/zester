#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Path hack.
import sys
import os
sys.path.insert(0, os.path.abspath(os.pardir))

import unittest

import fixtures
from fixtures.hnclient import HNClient
from fixtures.weather_client import WeatherClient


class ZesterTestSuite(unittest.TestCase):
    """Zester test cases."""

    def test_multi_client(self):
        hn_snapshot = os.path.join(fixtures.__path__[0], 'hn_snapshot.html')
        client = HNClient(url=hn_snapshot)
        stories = client.process()
        assert stories
        assert stories[0].title == "What Twitter could have been"
        assert (stories[0].link ==
            "http://daltoncaldwell.com/what-twitter-could-have-been")
        assert stories[0].points == "200"

    def test_single_client(self):
        weather_snapshot = os.path.join(fixtures.__path__[0],
                                                    'weather-gov.html')
        weather_snapshot += "?lat={lat}&lng={lng}"
        client = WeatherClient(lat=40.7143528, lng=-74.0059731,
                                                    url=weather_snapshot)
        curr_weather = client.process()
        assert curr_weather
        assert curr_weather.temperature == u'80\xb0F'
        assert curr_weather.humidity == "58%"
        assert curr_weather.heat_index == u'82\xb0F (28\xb0C)'
