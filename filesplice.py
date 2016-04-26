#!/usr/bin/env python

import csv
import os.path
from itertools import islice

with open("RollNo-DOB-2.csv", 'rb') as infh:
	reader = csv.reader(infh)
	records = 0

	for row in reader:
		records = records + 100000
		filename = "RollNo-DOB-2-" + str(records) + ".csv"
		filename = os.path.join('/Users/Ashutosh/Desktop/', filename)
		with open (filename, 'wb') as outfh:
			writer = csv.writer(outfh)
			writer.writerow(row)
			writer.writerows(islice(reader, 100000))