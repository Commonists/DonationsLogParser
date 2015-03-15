#!/usr/bin/python
"""
daily_parser.py
	the daily parser allows to export daily results for a given month.
"""
from HTMLParser import HTMLParser


class DonationsParser(HTMLParser, object):
	"""
	HTML parser for the donations log of Wikimedia France
	"""
	def __init__(self, year, month):
		super(DonationsParser, self).__init__()
		self.year = year
		self.month = month
		self.status = 0
		self.current_line = ""
		self.donations = dict()

	def handle_starttag(self, tag, attrs):
		if tag == 'td':
			for attr, val in attrs:
				if attr == 'colspan' and val == '4':
					self.status = 1
		if tag == 'em' and self.status == 1:
			self.status = 2

	def handle_endtag(self, tag):
		if tag == 'em' and self.status == 2:
			self.status = 1
		if tag == 'td' and self.status == 1:
			self.status = 0
			if self.current_line.startswith('Total des dons pour le'):
				data = self.parse_donation_line(self.current_line)
				day = "%02d" % (int(data[0]))
				result = dict()
				result['quantity'] = int(data[1])
				result['sum'] = int(data[2])
				result['avg'] = round(float(result['sum']) / float(result['quantity']), 2)
				self.donations[day] = result
			self.current_line = ""

	def handle_data(self, data):
		if self.status == 2:
			self.current_line += data

	def parse_donation_line(self, line):
		import re
		# removing white space in order to parse correctly numbers over 999
		s = line.replace(' ', '')
		data = re.findall(r'\d+', s)
		return data

	def get_csv(self):
		"""
		Print donations as CSV
		"""
		csv = ''
		csv += "'day', 'sum', 'quantity', 'avg'\n"
		for k in sorted(self.donations.keys()):
			data = self.donations[k]
			csv += "'%04d-%02d-%s', %d, %d, %.2f\n" % \
				(self.year, self.month, k, data['sum'], data['quantity'], data['avg'])
		return csv

	def get_js(self, js_var_name):
		"""
		print donations to JS array
		"""
		n = len(self.donations.keys())
		i = 0
		js = ''
		js += "var %s = [\n" % (js_var_name)
		js += "['day', 'sum', 'quantity', 'avg'],\n"
		for k in sorted(self.donations.keys()):
			i += 1
			data = self.donations[k]
			print_format = "['%04d-%02d-%s', %d, %d, %.2f],\n"
			if i == n:
				print_format = "['%04d-%02d-%s', %d, %d, %.2f]\n"  # no comma for the last row
			js += print_format \
				% (self.year, self.month, k, data['sum'], data['quantity'], data['avg'])
		js += "];"
		return js


def url_from_args(year, month):
	"""
	Generate Donation log url from args
		e.g. https://dons.wikimedia.fr/journal/2013-12
	"""
	return "https://dons.wikimedia.fr/journal/%04d-%02d" % (year, month)


def get_page(url):
	"""
	Get the page based on URL and return it's content as a string.
	"""
	import urllib
	return urllib.urlopen(url).read()


def export_annual_result(donations):
	"""
	Export and aggregate entire year resuls.
	"""
	money = 0
	donators = 0
	report = ''
	report += "%d days of donations" % (len(donations.keys()))
	for k in donations.keys():
		money += donations[k]['sum']
		donators += donations[k]['quantity']
	report += "Total donations: %d\nTotal donators: %d" % (money, donators)
	return report


def aggregate_on_the_whole_year(year, month):
	"""Aggregate on the whole year."""
	results = dict()
	for month in range(1, 13):
		content = get_page(url_from_args(year, month))
		donations_parser = DonationsParser(year, month)
		donations_parser.feed(content)
		for k in donations_parser.donations.keys():
			key = "%04d-%02d-%s" % (year, month, k)
			results[key] = donations_parser.donations[k]
	print export_annual_result(results)


def main():
	"""
	Main function of the script parse_donations.py.
	"""
	from argparse import ArgumentParser
	description = "Parse donations data from dons.wikimedia.fr"
	parser = ArgumentParser(description=description)
	parser.add_argument("-a", "--all",
						action="store_true",
						dest="all",
						required=False,
						help="Aggregate results of the whole year")
	parser.add_argument("-y", "--year",
    					type=int,
                        dest="year",
						metavar="YEAR",
						required=True,
                        help="Donation year")
	parser.add_argument("-m", "--month",
    					type=int,
                        dest="month",
						metavar="MONTH",
						required=False,
                        help="Donation month")
	parser.add_argument("-j", "--js",
    					type=str,
                        dest="js",
						metavar="JS",
						required=False,
                        help="Name of JS var to export to")
	args = parser.parse_args()
	# checking args
	if args.year < 0 or args.year > 9999:
		raise ValueError('year should be between 0 and 9999 (instead of %d)' % (args.year))
	if args.all:
		aggregate_on_the_whole_year(args.year, args.month)
	else:
		if args.month < 1 or args.month > 12:
			raise ValueError('month should be between 1 and 12 (instead of %d)' % (args.month))

		content = get_page(url_from_args(args.year, args.month))
		donations_parser = DonationsParser(args.year, args.month)
		donations_parser.feed(content)
		if args.js:
			print donations_parser.get_js(args.js)
		else:
			print donations_parser.get_csv()

if __name__ == "__main__":
	main()
