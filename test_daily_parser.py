#!/usr/bin/env python
# -*- coding: latin-1 -*-

"""Unit tests."""

import unittest
from daily_parser import url_from_args, DonationsParser


class TestDailyParser(unittest.TestCase):

    """Testing methods from daily_parser."""

    def test_url_from_args(self):
        output = url_from_args(2014, 1)
        expected = 'https://dons.wikimedia.fr/journal/2014-01'
        self.assertEqual(output, expected)


class TestDonationsParser(unittest.TestCase):

    """Testing DonationsParser class."""

    def setUp(self):
        self.donations_parser = DonationsParser(2014, 01)
        donations_data = {
            '01': {'sum': 370, 'avg': 46.25, 'quantity': 8},
            '02': {'sum': 5682, 'avg': 132.14, 'quantity': 43}
        }
        self.donations_parser.donations = donations_data

    def test_get_csv(self):
        expected = """'day', 'sum', 'quantity', 'avg'
'2014-01-01', 370, 8, 46.25
'2014-01-02', 5682, 43, 132.14
"""
        output = self.donations_parser.get_csv()
        self.assertEqual(output, expected)
