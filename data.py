#!/usr/bin/python
""" Manages donation database. """

import sqlite3


class Donation:

    def __init__(self, date, name, donation, comment, db=None):
        # checking datetime format
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%s')
        except ValueError:
            raise ValueError(
                "%s should be in YYYY-mm-dd HH:MM:ss format" % date)
        # save object after checking data
        self.date = date
        self.name = name
        self.donation = float(donation)
        self.comment = comment

    def save(self):
        """ Insert a donation into a DonationDatabase donations table. """
        if db is not None:
            db.insert(self)

    def __str__(self):
        str_format = """'date': %s, 'name': %s, 'donation': %s, 'comment': %s"""
        return str_format % (self.date, self.name, self.donation, self.comment)

    def __repr__(self):
        return '\n'.join([self.date, self.name, self.donation, self.comment])


class DonationDatabase:

    """ Manages the donation database. """

    def __init__(self, filename, is_drop_table=False):
        """ Init the database object.

        Args:
            filename (string): name of the sqlite database file.
            is_drop_table (bool): whether to drop the existing database or not.
        """
        self.connection = sqlite3.connect(filename)
        self.cursor = self.connection.cursor()

        # table creation
        if is_drop_table:
            self.cursor.execute("""DROP TABLE donations""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS donations
                                (date, name, donation, comment)""")
        self.connection.commit()

    def insert(self, donation):
        """ Adds a donation to the database. """
        t = (donation.date, donation.name, donation.donation, donation.comment)
        self.cursor.execute("""INSERT INTO donations VALUES (?, ?, ?, ?)""", t)
        self.connection.commit()

    def listall(self):
        """ Returns a list of all the donation in the database. """


def main():
    """ Main function of the scripts."""
    db = DonationDatabase("dons.db")

    db.insert('2014-05-06 12:00', "Pi", 50.0, "I love wiki")
    db.insert('2014-06-08 14:15', "Te", 15, "Yeah \o/")

if __name__ == '__main__':
    main()
