#!/usr/bin/python
""" Manages donation database. """

import datetime
import sqlite3


class Donation:

    """ Donation represents a donation in the Donations Log.

    Attributes:
        date (str): Date in YYYY-mm-dd HH:MM:SS format.
        name (str): Donator name
        donation (float): Value of the donation in Euros
        comment (str): Free comment by the donator to appear in the Log
    """

    DATE_FIELD = 0
    NAME_FIELD = 1
    DONATION_FIELD = 2
    COMMENT_FIELD = 3

    def __init__(self, date, name, donation, comment, db=None):
        """ Creates a Donation

        Args:
            date (str): Date in YYYY-mm-dd HH:MM:SS format.
            name (str): Donator name
            donation (str): Value of the donation in Euros
            comment (str): Free comment by the donator to appear in the Log
            db (data.DonationDatabase, optional): DonationDatabase to save the
                donation entry.

        Raises:
            ValueError:
                when date is not a YYYY-mm-dd HH:MM:SS or
                when donation is not a convertible to float value
        """
        # checking datetime format
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            raise ValueError(
                "%s should be in YYYY-mm-dd HH:MM:SS format" % date)
        # save object after checking data
        self.date = date
        self.name = name
        self.donation = float(donation)
        self.comment = comment
        self.db = db

    @classmethod
    def fromtuple(cls, t):
        """ Create a donation from a tuple.

        Example:
            >> d = Donation(('2014-06-08 14:15:56', 'John', 15, 'Thank you'))
            data.Donation('2014-06-08 14:15:56', 'John', 15, 'Thank you')
        """
        return cls(t[Donation.DATE_FIELD],
                   t[Donation.NAME_FIELD],
                   t[Donation.DONATION_FIELD],
                   t[Donation.COMMENT_FIELD])

    def totuple(self):
        """ Returns a tuple from the donation object. 

        Note:
            Handy to save into db.

        Example:
            >> d = Donation('2014-06-08 14:15:56', 'John', 15, 'Thank you')
            >> d.totuple()
            ('2014-06-08 14:15:56', 'John', 15, 'Thank you')
        """
        return (self.date, self.name, self.donation, self.comment)

    def save(self):
        """ Insert a donation into a DonationDatabase donations table. """
        if self.db is not None:
            self.db.insert(self)

    def __repr__(self):
        """ Representation of the object. """
        return "data.Donation('%s', '%s', %s, '%s')" % (self.date,
                                                        self.name,
                                                        str(self.donation),
                                                        self.comment)


class DonationDatabase:

    """ Manages the donation database. 

    Attributes:
        connection (sqlite3.connection): sqlite database
        cursor (sqlite3.cursor): python database cursor.
    """

    def __init__(self, filename, drop_data_on_create=False):
        """ Init the database object.

        Args:
            filename (string): name of the sqlite database file.
            drop_data_on_create (bool, optional):
                whether to drop the existing database or not on creation.
                default: False
        """
        self.connection = sqlite3.connect(filename)
        self.cursor = self.connection.cursor()

        # table creation
        if drop_data_on_create:
            self.cursor.execute("""DROP TABLE donations""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS donations
                                (date, name, donation, comment)""")
        self.connection.commit()

    def insert(self, donation):
        """ Adds a donation to the database. 

        Args:
            donation (Donation): insert a donation into the database.
        """
        t = donation.totuple()
        self.cursor.execute("""INSERT INTO donations VALUES (?, ?, ?, ?)""", t)
        self.connection.commit()

    def listall(self):
        """ List of all the donation in the database. 

        Returns:
            list: All donations from the database
        """
        self.cursor.execute("""SELECT
            date, name, donation, comment
            FROM donations""")
        all_result = self.cursor.fetchall()
        list_donations = []
        for d in all_result:
            donation = Donation.fromtuple(d)
            donation.db = self
            list_donations.append(donation)
        return list_donations


def main():
    """ Main function of the scripts."""
    db = DonationDatabase("dons.db", drop_data_on_create=True)

    donation1 = Donation(
        '2014-05-06 12:00:05', "Pi", 50.0, "I love wiki", db=db)
    donation2 = Donation('2014-06-08 14:15:56', "Te", 15, "Yeah \o/", db=db)

    donation1.save()
    donation2.save()

    print db.listall()

if __name__ == '__main__':
    main()
