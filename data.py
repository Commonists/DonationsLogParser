#!/usr/bin/python
""" Manages donation database. """

import datetime
import sqlite3


class Donation:

    DATE_FIELD = 0
    NAME_FIELD = 1
    DONATION_FIELD = 2
    COMMENT_FIELD = 3

    def __init__(self, date, name, donation, comment, db=None):
        # checking datetime format
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
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

    def __repr__(self):
        return ';'.join([self.date, self.name, str(self.donation), self.comment])


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
        self.cursor.execute("""SELECT
            date, name, donation, comment
            FROM donations""")
        all_result = self.cursor.fetchall()
        list_donations = []
        for d in all_result:
            list_donations.append(Donation(d[Donation.DATE_FIELD],
                                           d[Donation.NAME_FIELD],
                                           d[Donation.DONATION_FIELD],
                                           d[Donation.COMMENT_FIELD],
                                           db=self))
        return list_donations


def main():
    """ Main function of the scripts."""
    db = DonationDatabase("dons.db", is_drop_table=True)

    db.insert(Donation('2014-05-06 12:00:05', "Pi", 50.0, "I love wiki"))
    db.insert(Donation('2014-06-08 14:15:56', "Te", 15, "Yeah \o/"))

    print db.listall()

if __name__ == '__main__':
    main()
