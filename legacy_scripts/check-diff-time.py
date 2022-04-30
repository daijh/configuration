#!/usr/bin/python

import sys
import getopt
import os
import time
import re
import operator
import sqlite3
import csv

if __name__ == '__main__':

	try:
		options, arguments = getopt.getopt(sys.argv[1:], "hdpso:", [])
	except getopt.GetoptError, error:
		PrintUsage()

	if len(arguments) != 1:
		PrintUsage()

	output_file = ''

	for option, value in options:
		if option == "-h":
			PrintUsage()
		elif option == "-d":
			DEBUG_ENABLED = True
		elif option == "-p":
			DEBUG_PERF_ENABLED = True
		elif option == "-s":
			DB_ENABLED = True
		elif option == "-o":
			output_file = value + ".csv"
		else:
			PrintUsage()

	if(len(output_file) == 0):
		output_file = 'result' + ".csv"

	input_file = arguments[0]

	fd = file(input_file)

	timestamp_list = []
	for line in fd.readlines():
		if not re.search(r'tracing_mark_write.*Audio-AccessUnit-timeUs', line):
			continue

		print line

		items = line.strip().split('|')
	
		print items[-1]

		#timestamp = int(items[-1])
		#print timestamp
	
		items = items[-1].split('\\')
	
		timestamp = int(items[0])
		print timestamp

		timestamp_list += [timestamp]
		
	previous_t = 0
	for t in timestamp_list:
		if not previous_t == 0:
			print (t - previous_t) / 1000.0

		previous_t = t




