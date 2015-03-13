#!/usr/bin/env python
# -*- coding: latin-1 -*-

"""Unit tests."""

import unittest
from daily_parser import url_from_args


class TestDailyParser(unittest.TestCase):

    """Testing methods from daily_parser."""

    def test_url_from_args(self):
        output = url_from_args(2014, 1)
        expected = 'https://dons.wikimedia.fr/journal/2014-01'
        self.assertEqual(output, expected)
