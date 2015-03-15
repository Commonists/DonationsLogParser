#!/usr/bin/python
""" Log parser. """
from HTMLParser import HTMLParser
import urllib


class DailyParser(HTMLParser):

    """
    HTML parser for the donations log of Wikimedia France

    Attributes:
        status (int): status variable of the parser.
        donations (list data.Donation): list of donations read.
    """

    START_PARSER = 0
    FOUND_DONATION_TABLE = 1
    READ_HOURS = 2
    READ_DONATOR = 3
    READ_DONATION = 4
    END_OF_DONATION_TABLE = 5

    def __init__(self):
        super(DonationsParser, self).__init__()
        self.status = DailyParser.START_PARSER
        self.donations = []

    def handle_starttag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass


class LogParser:

    def __init__(self):
        self.parser = DailyParser()

    @staticmethod
    def daypage(day):
        """ Returns the page content containing the donations from a specific 
        day.

        Args:
            day (datetime.date): day to fetch donation.

        Returns:
            str: page content with the donation of the day specified as args.
        """
        url_args = date.strftime("%Y-%m-%d")
        url = "https://dons.wikimedia.fr/journal/%s" % url_args
        return urllib.urlopen(url).read()

    def fetchday(self, day):
        """ Returns donations from a day. """
        day_content = self.daypage(day)
        self.parser.feed(day_content)
