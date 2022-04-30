#!/usr/bin/python -E

import sys
import os
import re

def gettimestamp(line):
	tokens = line.split(':')

	#for token in tokens:
	#	print token

	#tokens = tokens[0].split()[-1]

	#for token in tokens:
	#	print token

	timestamp = tokens[0].split()[-1]

	return float(timestamp)

if __name__ == '__main__':
	if(len(sys.argv) != 2):
		print 'Usage: ', sys.argv[0], "systrace.html"
		sys.exit(1)

	if not os.path.isfile(sys.argv[1]):
		print "Error: fils does not exist, "+sys.argv[1]
		sys.exit(1)

	path = sys.argv[1]
	fd = file(path)

	state_machine = []

	state_machine += []

	state_machine += [{
		'name': 'System Rec Input',

		'pattern': 'tracing_mark_write.*C\|.*\|iq|\1',

		'raw': None,
		'timestamp': None,

		}]

	state_machine += [{
		'name': 'CameraHal Set Preview Buffer',

		'pattern': 'CamHAL_PREVIEW.*tracing_mark_write.*B\|.*\|setBuffersDimensions',

		'raw': None,
		'timestamp': None,
		}]

	state_machine += [{
		'name': 'CameraHal Enqueue First Frame',

		'pattern': 'CamHAL_PREVIEW.*tracing_mark_write.*B\|.*\|queueBuffer',

		'raw': None,
		'timestamp': None,
		}]

	state_machine += [{
		'name': 'SurfaceFlinger Post Framebuffer',

		'pattern': 'tracing_mark_write.*B\|.*\|postFramebuffer',

		'raw': None,
		'timestamp': None,
		}]

	state_machine += [{
		'name': 'SurfaceFlinger Page Flip Done',

		'pattern': 'tracing_mark_write.*B\|.*\|page_flip_handler',

		'raw': None,
		'timestamp': None,
		}]

	state = 0
	time_begin = 0
	time_end = 0

	for line in fd.readlines():
		if state >= len(state_machine):
			break

		if re.search(state_machine[state]['pattern'], line):
			#print line
			#print gettimestamp(line)

			state_machine[state]['timestamp'] = gettimestamp(line)
			state += 1

		'''
		if stage == 0:
			if re.search('tracing_mark_write.*C\|.*\|iq|\1', line):
				print line
				print gettimestamp(line)

				stage += 1

		if stage == 1:
			#CamHAL_PREVIEW-3546  ( 2107) [003] ...1    60.004280: tracing_mark_write: B|2107|setBuffersDimensions\n\
			#if re.search('CamHAL_PERVIEW.*tracing_mark_write.*B\|.*\|setBuffersDimensions', line):
			if re.search('CamHAL_PREVIEW.*tracing_mark_write.*B\|.*\|setBuffersDimensions', line):
				print line
				print gettimestamp(line)

				stage += 1

		if stage == 2:
			if re.search('CamHAL_PREVIEW.*tracing_mark_write.*B\|.*\|queueBuffer', line):
				print line
				print gettimestamp(line)

				stage += 1

		if stage == 3:
			if re.search('tracing_mark_write.*C\|.*\|com.android.camera2/com.android.camera.CameraLauncher\|1', line):
				print line
				print gettimestamp(line)

				stage += 1

		if stage == 4:
			if re.search('tracing_mark_write.*B\|.*\|postFramebuffer', line):
				print line
				print gettimestamp(line)

				stage += 1

		if stage == 5:
			if re.search('tracing_mark_write.*B\|.*\|page_flip_handler', line):
				print line
				print gettimestamp(line)

				stage += 1
		'''

	duration_ms = (state_machine[-1]['timestamp'] - state_machine[0]['timestamp']) * 1000
	print 'Total duration: ',  duration_ms, 'ms'

	for i in range(len(state_machine)):
		if i == 0:
			continue

		duration_ms = (state_machine[i]['timestamp'] - state_machine[i - 1]['timestamp']) * 1000

		print 'From ', state_machine[i-1]['name'], ' To ', state_machine[i]['name'], ' : ', duration_ms, 'ms'

