DonationsLogParser
==================

Donations Log Parser for Wikimedia France. It allows to export donations log by month into CSV or JS array.

Usage
-----
In order to export as CSV data of december 2013 into data/donations-2013-12.csv just run
```
python daily_parser.py -y 2013 -m 12 > data/donations-2013-12.csv
```

In order to export as JS array the data of december 2013 into data/donations-2013-12.js in the var named donations12Data just run
```
python daily_parser.py -y 2013 -m 12 -j donations12Data > data/donations-2013-12.js
```
