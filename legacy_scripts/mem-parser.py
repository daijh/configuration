#! /usr/bin/python

# @author	jianhui.j.dai@intel.com
# @brief	parse procrank, procmem result for memory footprint
# @version	0.1
# @date		2014/07/03

import os
import sys
import csv
import getopt

def PrintUsage():
	print "  Usage: " + sys.argv[0] + "  [options]  /path/to/mem/directory"
	print "      -h"
	print "          help"
	print "      -d"
	print "          debug"
	print "      -o"
	print "          output file name, default is mem_result.csv"
	sys.exit(1)

if __name__ == '__main__':
	debug_enabled = False

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
			debug_enabled = True
		elif option == "-o":
			output_file = value + ".csv"
		else:
			PrintUsage()

	if(len(output_file) == 0):
		output_file = 'mem-result.csv'

	input = arguments[0]

	PROCRANK = input + '/procrank.txt'
	SF_PROCMEM = input + '/surfaceflinger-procmem.txt'
	MEDIA_PROCMEM = input + '/mediaserver-procmem.txt'
	GEM_OBJECTS = input + '/i915_gem_objects.txt'

	patterns = []

	patterns += [{
		'key': 'TOTAL',
		'item': '1',
		'name': 'PSS',
		'file': PROCRANK,

		'format': ['PSS', None, None, 'VALUE', None, None]
		}]
	patterns += [{
		'key': 'com.android',
		'item': '4',
		'name': 'com.android',
		'file': PROCRANK,

		'format': [None, 'com.android', None, None, 'VALUE', None]
		}]

	patterns += [{
		'key': 'com.android.launcher',
		'item': '4',
		'name': 'com.android.launcher',
		'file': PROCRANK,

		'format': [None, None, 'com.android.launcher', None, None, 'VALUE']
		}]
	patterns += [{
		'key': 'com.android.systemui',
		'item': '4',
		'name': 'com.android.systemui',
		'file': PROCRANK,

		'format': [None, None, 'com.android.systemui', None, None, 'VALUE']
		}]
	patterns += [{
		'key': 'com.android.phone',
		'item': '4',
		'name': 'com.android.phone',
		'file': PROCRANK,

		'format': [None, None, 'com.android.phone', None, None, 'VALUE']
		}]
	patterns += [{
		'key': 'com.android.camera2',
		'item': '4',
		'name': 'com.android.camera2',
		'file': PROCRANK,

		'format': [None, None, 'com.android.camera2', None, None, 'VALUE']
		}]

	patterns += [{
		'key': 'com.android.chrome',
		'item': '4',
		'name': 'com.android.chrome',
		'file': PROCRANK,

		'format': [None, None, 'com.android.chrome', None, None, 'VALUE']
		}]
	patterns += [{
		'key': 'com.google',
		'item': '4',
		'name': 'com.google',
		'file': PROCRANK,

		'format': [None, 'com.google', None, None, 'VALUE', None]
		}]
	patterns += [{
		'key': 'com.google.process.gapps',
		'item': '4',
		'name': 'com.google.process.gapps',
		'file': PROCRANK,

		'format': [None, None, 'com.google.process.gapps', None, None, 'VALUE']
		}]
	patterns += [{
		'key': 'com.google.process.location',
		'item': '4',
		'name': 'com.google.process.location',
		'file': PROCRANK,

		'format': [None, None, 'com.google.process.location', None, None, 'VALUE']
		}]
	patterns += [{
		'key': 'com.google.android.gms',
		'item': '4',
		'name': 'com.google.android.gms',
		'file': PROCRANK,

		'format': [None, None, 'com.google.android.gms', None, None, 'VALUE']
		}]
	patterns += [{
		'key': 'com.google.android.inputmethod.latin',
		'item': '4',
		'name': 'com.google.android.inputmethod.latin',
		'file': PROCRANK,

		'format': [None, None, 'com.google.android.inputmethod.latin', None, None, 'VALUE']
		}]
	patterns += [{
		'key': 'com.google.android.gallery3d',
		'item': '4',
		'name': 'com.google.android.gallery3d',
		'file': PROCRANK,

		'format': [None, None, 'com.google.android.gallery3d', None, None, 'VALUE']
		}]
	patterns += [{
		'key': 'com.google.android.GoogleCamera',
		'item': '4',
		'name': 'com.google.android.GoogleCamera',
		'file': PROCRANK,

		'format': [None, None, 'com.google.android.GoogleCamera', None, None, 'VALUE']
		}]
	patterns += [{
		'key': 'com.intel',
		'item': '4',
		'name': 'com.intel',
		'file': PROCRANK,

		'format': [None, 'com.intel', None, None, 'VALUE', None]
		}]
	patterns += [{
		'key': 'zygote',
		'item': '4',
		'name': 'zygote',
		'file': PROCRANK,

		'format': [None, 'zygote', None, None, 'VALUE', None]
		}]
	patterns += [{
		'key': 'system_server',
		'item': '4',
		'name': 'system_server',
		'file': PROCRANK,

		'format': [None, 'system_server', None, None, 'VALUE', None]
		}]
	patterns += [{
		'key': 'coreu',
		'item': '4',
		'name': 'coreu',
		'file': PROCRANK,

		'format': [None, 'coreu', None, None, 'VALUE', None]
		}]
	patterns += [{
		'key': 'drmserver',
		'item': '4',
		'name': 'drmserver',
		'file': PROCRANK,

		'format': [None, 'drmserver', None, None, 'VALUE', None]
		}]
	patterns += [{
		'key': 'mediaserver',
		'item': '4',
		'name': 'mediaserver',
		'file': PROCRANK,

		'format': [None, 'mediaserver', None, None, 'VALUE', None]
		}]
	# media procmem
	patterns += [{
		'key': 'heap|malloc',
		'item': '3',
		'name': 'media-heap',
		'file': MEDIA_PROCMEM,

		'format': [None, None, 'heap', None, None, 'VALUE']
		}]
	patterns += [{
		'key': '\/drm|dri',
		'item': '3',
		'name': 'media-gem_mapped',
		'file': MEDIA_PROCMEM,

		'format': [None, None, 'gem_mapped', None, None, 'VALUE']
		}]
	patterns += [{
		'key': '\.so',
		'item': '3',
		'name': 'media-shared_libs',
		'file': MEDIA_PROCMEM,

		'format': [None, None, 'libs', None, None, 'VALUE']
		}]


	'''
	patterns += [{
		'key': 'i965_drv_video\.so',
		'item': '3',
		'name': 'media-i965_drv_video.so',
		'file': MEDIA_PROCMEM,

		'format': [None, None, 'i965_drv_video.so', None, None, 'VALUE']
		}]
	'''

	patterns += [{
		'key': 'surfaceflinger',
		'item': '4',
		'name': 'surfaceflinger',
		'file': PROCRANK,

		'format': [None, 'surfaceflinger', None, None, 'VALUE', None]
		}]

	# surfaceflinger procmem
	patterns += [{
		'key': 'heap|malloc',
		'item': '3',
		'name': 'surfaceflinger-heap',
		'file': SF_PROCMEM,

		'format': [None, None, 'heap', None, None, 'VALUE']
		}]
	patterns += [{
		'key': '\/drm|dri',
		'item': '3',
		'name': 'surfaceflinger-gem_mapped',
		'file': SF_PROCMEM,

		'format': [None, None, 'gem_mapped', None, None, 'VALUE']
		}]
	patterns += [{
		'key': '\.so',
		'item': '3',
		'name': 'surfaceflinger-shared_libs',
		'file': SF_PROCMEM,

		'format': [None, None, 'libs', None, None, 'VALUE']
		}]

	'''
	patterns += [{
		'key': 'i965_drv_video\.so',
		'item': '3',
		'name': 'surfaceflinger-i965_drv_video',
		'file': SF_PROCMEM,

		'format': [None, None, 'i965_drv_video.so', None, None, 'VALUE']
		}]
	'''

	patterns += [{
		'key': 'RAM:',
		'item': '6',
		'name': 'k-buffers',
		'file': PROCRANK,

		'format': ['k-buffers', None, None, 'VALUE', None, None]
		}]
	patterns += [{
		'key': 'RAM:',
		'item': '12',
		'name': 'k-slab',
		'file': PROCRANK,

		'format': ['k-slab', None, None, 'VALUE', None, None]
		}]

	patterns += [{
		'key': 'RAM:',
		'item': '10',
		'name': 'k-gem',
		'file': PROCRANK,

		'format': ['k-gem', None, None, 'VALUE', None, None]
		}]
	'''
	patterns += [{
		'key': 'fault',
		'item': '5',
		'name': 'k-gem-fault',
		'file': GEM_OBJECTS,

		'format': ['k-gem-fault', None, None, 'VALUE', None, None]
		}]
	'''

	total = 0
	for p in patterns:
		if debug_enabled:
			cmd = "awk 'BEGIN { sum = 0 } /" + p['key'] + "/ {print $0, sum += $" + p['item'] + " };END {print \"" + p['name'] + " is:\", sum}' "  + p['file']
			ret = os.popen(cmd).read()
			print cmd
			print "Detail: ", ret

		cmd = "awk 'BEGIN { sum = 0 } /" + p['key'] + "/ {sum += $" + p['item'] + " };END {print sum}' "  + p['file']
		ret = os.popen(cmd).read()

		if debug_enabled:
			print cmd
			print "Value: ", ret

		index = p['format'].index('VALUE')

		if p['name'] == 'k-gem-fault':
			sizeKB = float(ret) / 1024
			p['format'][index] = "%.2fMB" % (float(ret) / 1024 / 1024)

			if index == 3:
				total -= int(sizeKB)

		else:
			sizeKB = float(ret)
			p['format'][index] = "%.2fMB" % (float(ret) / 1024)

			if index == 3:
				total += sizeKB

	# add total
	patterns[0:0] = [{
		'key': None,
		'item': None,
		'name': None,
		'file': None,

		'format': ['Total', None, None, "%.2fMB" % (float(total) / 1024), None, None]
		}]

	# write output
	fp = file(output_file, 'wb')
	writer = csv.writer(fp)

	for p in patterns:
		if debug_enabled:
			print p['format']

		writer.writerow(p['format'])

	sys.exit(1)
