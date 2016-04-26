#!/usr/bin/env python
import mechanize
import csv
from bs4 import BeautifulSoup
import os.path
from itertools import islice
import time

def crawlToCSV(csvfile):

	placeHolder = []
	i = 0

	for row in csv_f:
		regno = row[0]
		dob = row[1]

		i = i + 1

		print (str(i) + " row(s) read")

		# mechanize code to input form content and get to the results page
		br = mechanize.Browser()
		br.set_handle_robots(False)
		br.addheaders = [('User-agent', 'Firefox')]

		tried = 0
		while True:
			try:
				br.open(webURL)
				br._factory.is_html = True

			except (mechanize.HTTPError, mechanize.URLError) as e:
				tried += 1
				if isinstance (e, mechanize.HTTPError):
					print e.code
				else:
					print e.reason.args
				if tried > 10:
					exit()
				time.sleep(15)
				continue
			break

		print ("Site Reachable!")

		tried = 0
		while True:
			try:
				br.select_form('FrontPage_Form1')
				br.form['regno'] = regno
				br.form['dob'] = dob
				time.sleep(0.0001)
				br.submit()

			except (mechanize.BrowserStateError, mechanize.HTTPError, mechanize.URLError) as e:
				tried += 1
				if isinstance (e, mechanize.BrowserStateError):
					print ("BrowserStateError")
					time.sleep(15)
					tried = 0
					while True:
						try:
							br.open(webURL)
							br._factory.is_html = True

						except (mechanize.HTTPError, mechanize.URLError) as e:
							tried += 1
							if isinstance (e, mechanize.HTTPError):
								print e.code
							else:
								print e.reason.args
							if tried > 10:
								exit()
							time.sleep(15)
							continue
						break

					print ("Site Reachable Again!")

				elif isinstance (e, mechanize.HTTPError):
					print e.code
				else:
					print e.reason.args
				if tried > 10:
					exit()
				time.sleep(15)
				continue
			break

		print ("Form Submitted with Roll No " + regno)

		# getting the results into beautifulsoup
		soup = BeautifulSoup(br.response(), "lxml")

		try:
			# Parsing Roll No
			rollno = soup('table')[5].findAll('tr')[0].findAll('td')[1].string.strip()

			# Parsing All India Percentile Score in JEE (Main) 2015
			#percentile_rank = soup('table')[7].b.b.string

			# Parsing JEE (Main) Paper I Score
			phys = soup('table')[8].findAll('tr')[2].findAll('td')[2].b.string.strip()
			chem = soup('table')[8].findAll('tr')[3].findAll('td')[1].b.string.strip()
			math = soup('table')[8].findAll('tr')[4].findAll('td')[1].b.string.strip()
			total = soup('table')[8].findAll('tr')[5].findAll('td')[1].b.string.strip()
			norm = soup('table')[8].findAll('tr')[2].findAll('td')[3].b.string.strip()

			# Parsing JEE (Main) Paper II Score
			#math2 = soup('table')[8].findAll('tr')[6].findAll('td')[2].b.string.strip()
			#apt = soup('table')[8].findAll('tr')[6].findAll('td')[1].b.string.strip()
			#draw = soup('table')[8].findAll('tr')[7].findAll('td')[1].b.string.strip()
			#total2 = soup('table')[8].findAll('tr')[8].findAll('td')[1].b.string.strip()

			# Parsing All India Rank
			cat1 = soup('table')[10].findAll('tr')[2].findAll('td')[1].string.strip()
			cat2 = soup('table')[10].findAll('tr')[2].findAll('td')[2].string.strip()
			cat3 = soup('table')[10].findAll('tr')[2].findAll('td')[3].string.strip()
			cat4 = soup('table')[10].findAll('tr')[2].findAll('td')[4].string.strip()
			cat5 = soup('table')[10].findAll('tr')[2].findAll('td')[5].string.strip()
			cat6 = soup('table')[10].findAll('tr')[2].findAll('td')[6].string.strip()
			cat7 = soup('table')[10].findAll('tr')[2].findAll('td')[7].string.strip()
			cat8 = soup('table')[10].findAll('tr')[2].findAll('td')[8].string.strip()

			entry = (rollno, phys, chem, math, total, norm, cat1, cat2, cat3, cat4, cat5, cat6, cat7, cat8)

		except IndexError:
			print("------Record Skipped------")
			entry = (regno, "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-")

		placeHolder.append(entry)

	return placeHolder

if __name__ == "__main__":
	masterFileName = "Inputs-1000.csv"
	webURL = 'http://cbseresults.nic.in/jee_main/jee_cbse_2015.htm'

	with open(masterFileName, 'rb') as infh:
		reader = csv.reader(infh)
		records = 0
		incr = 100

		for row in reader:
			records = records + incr
			fileName = "Inputs-1000-Batch-" + str(records) + ".csv"
			fileName = os.path.join('/Users/Ashutosh/Projects/cbsescraper/', fileName)
			with open (fileName, 'wb') as outfh:
				writer = csv.writer(outfh)
				writer.writerow(row)
				writer.writerows(islice(reader, incr))
			with open(fileName, "rb") as f:
				csv_f = csv.reader(f)
				print ("File " + fileName + " read")
				results = crawlToCSV(csv_f)
			with open("Output.csv", "ab") as csv_g:
				writeFile = csv.writer(csv_g)
				for result in results:
					writeFile.writerow(result)

				print ("Output.csv written successfully!")

