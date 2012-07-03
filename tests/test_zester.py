#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Path hack.
import sys
import os
sys.path.insert(0, os.path.abspath(os.pardir))

import unittest

import fixtures
from fixtures.hnclient import HNClient


class ZesterTestSuite(unittest.TestCase):
    """Zester test cases."""

    def test_base(self):
        hn_snapshot = os.path.join(fixtures.__path__[0], 'hn_snapshot.html')
        client = HNClient()
        client.url = hn_snapshot
        stories = client.process()
        assert stories
        assert stories[0].title == "What Twitter could have been"
        assert (stories[0].link ==
            "http://daltoncaldwell.com/what-twitter-could-have-been")
        assert stories[0].points == "200"
