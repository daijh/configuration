#! /usr/bin/python

# @author	jianhui.j.dai@intel.com 
# @brief	profile share library symbols size 
# @version	0.1 
# @date		2014/07/03

import os
import sys
import csv
import getopt
import re 

import operator
from operator import itemgetter, attrgetter  

def PrintUsage():
	print "  Usage: " + sys.argv[0] + "  [options]  /path/to/lib/directory"
	print "      -h"
	print "          help"
	print "      -d"
	print "          debug"
	print "      -o"
	print "          output path, default is disk-result"
	sys.exit(1)

if __name__ == '__main__':
	debug_enabled = False

	try:
		options, arguments = getopt.getopt(sys.argv[1:], "hdpso:", [])
	except getopt.GetoptError, error:
		PrintUsage()

	if len(arguments) != 1:
		PrintUsage()

	size_tool = 'size'
	strip_tool = 'strip'
	symbols_tool = 'nm -C -S --size-sort -r -t d'

	output_folder = 'disk-result'
	output_file = 'summary.csv'

	for option, value in options:
		if option == "-h":
			PrintUsage()
		elif option == "-d":
			debug_enabled = True
		elif option == "-o":
			output_folder = value
		else:
			PrintUsage()

	output_folder_stripped = output_folder + '/stripped'
	output_folder_symbols = output_folder + '/symbols'
	if not os.path.exists(output_folder):
		os.makedirs(output_folder)
		os.makedirs(output_folder_stripped)
		os.makedirs(output_folder_symbols)
	else:
		print 'Error:', output_folder, 'exists allready'
		sys.exit(1)

	input = arguments[0]

	result = [['Name', 'Size/byte', 'Stripped Size/byte', 'text', 'data', 'bss']]

	for root, dirs, files in os.walk(input):
		for fn in files:
			if re.match(r'.*\.so$', fn):

				# init
				item = [[None, 0, 0, 0, 0, 0]]

				# name
				item[0][0] = (root+'/'+fn).lstrip('./')

				# size
				size = os.path.getsize(os.path.join(root, fn))
				item[0][1] = int(size)

				# stripped size
				stripped_file = output_folder_stripped + '/' + fn + '_stripped'
				cmd = strip_tool + ' ' + root + '/' + fn + ' -o ' + stripped_file

				stream = os.popen(cmd)
				lines = stream.readlines()
				#print cmd
				#print lines

				if os.path.exists(stripped_file):
					stripped_size = os.path.getsize(os.path.join(stripped_file))
					item[0][2] = int(stripped_size)
				else:
					item[0][2] = int(size)

				# symbols
				symbols_file = output_folder_symbols + '/' + fn + '_symbols'
				cmd = symbols_tool + ' ' + root + '/' + fn + ' > ' + symbols_file

				stream = os.popen(cmd)
				lines = stream.readlines()
				#print cmd
				#print lines

				# text, data, bss
				cmd = size_tool + ' ' + root + '/' + fn

				stream = os.popen(cmd)
				lines = stream.readlines()
				#print cmd
				#print lines

				if len(lines) > 1:
					ret = lines[1].split()

					item[0][3] = int(ret[0])
					item[0][4] = int(ret[1])
					item[0][5] = int(ret[2])

				#print item

				result += item 

	#print result

	result.sort(key=operator.itemgetter(1), reverse=True)

	summary = [['All', 0, 0, 0, 0, 0]]

	for line in result[1:]:
		summary[0][1] += line[1]
		summary[0][2] += line[2]
		summary[0][3] += line[3]
		summary[0][4] += line[4]
		summary[0][5] += line[5]

	result += summary

	# write output
	fp = file(output_folder + '/' + output_file, 'wb')
	writer = csv.writer(fp)
	writer.writerows(result)

	print 'Done:', output_folder 

	sys.exit(1)
