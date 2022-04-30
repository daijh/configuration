#!/usr/bin/python

import sys
import getopt
import os
import time
import re
import operator
import sqlite3
import csv

DEBUG_ENABLED = False
DB_ENABLED = False
DEBUG_PERF_ENABLED = False

'''
Parser will parse HTML log of systrace/MVP,
1: read line
2: parse a line into a log entry(dict)
3: put each log entry in sqlite table
'''
class Parser:
	def __init__(self):
		# file path to systrace/MVP HTML file
		self.file_path = None

		# parse result
		self.results = []

		self.db_conn = 0

		self.__is_support_tgid = False

	def __del_(self):
		if(self.db_cursor):
			self.db_cursor.close()
		if(self.db_conn):
			self.db_conn.close()

	def is_support_tgid(self):
		return self.__is_support_tgid

	# parse a line
	def _parse_line(self, result):
		'''
		'''

		# a line of raw log, it's striped.
		raw = result['raw']

		#print raw
		# parse task & pid

		if self.__is_support_tgid:
			tokens = raw.split('(',1)

			tasks=tokens[0].split('-')
			#print 'str is: ', tasks
			if(len(tasks) > 2):
				result['task'] = '-'.join(tasks[0:-1])
			else:
				result['task'] = tasks[0]

			result['pid'] = tasks[-1]

			#print 'task is: ', result['task']
			#print 'pid is: ', result['pid']

			# tgid
			tokens = tokens[1].lstrip('(').split(')',1)
			result['tgid']= tokens[0]
		else:
			tokens = raw.split('[',1)

			tasks=tokens[0].split('-')
			#print 'str is: ', tasks
			if(len(tasks) > 2):
				result['task'] = '-'.join(tasks[0:-1])
			else:
				result['task'] = tasks[0]

			result['pid'] = tasks[-1]

			#print 'task is: ', result['task']
			#print 'pid is: ', result['pid']

			result['tgid']= None


		# cpu
		tokens = tokens[1].split()
		result['cpu'] = tokens[0].strip('[]')
		#print 'cpu is: ', result['cpu']

		#print "START=============="
		#print tokens
		#for t in tokens:
		#    print t
		#print "END=============="

		#timestamp(convert from second to microsecond)
		tokens[2] = tokens[2].rstrip(':')
		tmp = tokens[2].split('.')
		#print tmp
		#print tmp[0]
		#print tmp[1]
		try:
			result['timestamp'] = int(tmp[0]) * 1000000 + int( tmp[1] )
		except:
			if debug: print "Invalid log:" + raw
			return None

		# tracemark
		result['function']  = tokens[3].strip(': ')

		#print result['function']
		# MVP hard code function name - tracing_mark_write
		if result['function'] == 'tracing_mark_write' :
			miscs = tokens[4].split('|')
			#B|8888|VPHAL_PRI#E
			#MFX Engine-9999        [000] ...1  1914.418216: tracing_mark_write: B|9999|H264VLD_MODE_MIXED_TYPE\n\
					#if miscs[0] != 'B' and miscs[0] != 'E':
			#    print result['raw']
			#    raise 'Invalid Begin/End tag'

			i = 0
			while i < len(miscs) :
				if i == 0:
					result['tag'] = miscs[0]
					if result['tag'] != 'B' and result['tag'] != 'E' and result['tag'] != 'C':
						if debug:  print "Invalid tag(BE)"+raw
						pass

				if i == 1:
					result['thread'] = miscs[1]

				if i == 2:
					result['event'] = miscs[2]

				i += 1
		elif result['function'] == 'sched_switch':
			for i in range(4, len(tokens) ):
				if tokens[i] == '==>' : continue
				if tokens[i].find('=') < 0: continue

				(k,v) = tokens[i].split('=',2)
				if k == 'prev_comm' : result['prev_comm']  = v
				if k == 'prev_pid'  : result['prev_pid']    = int(v)
				if k == 'prev_prio' : result['prev_prio']   = v
				if k == 'prev_state': result['prev_state']  = v
				if k == 'next_comm' : result['next_comm']   = v
				if k == 'next_pid'  : result['next_pid']    = int(v)
				if k == 'next_prio' : result['next_prio']   = v

			'''
			TimedEventQueue-4374   [002] d...  1954.056536: sched_switch: prev_comm=TimedEventQueue prev_pid=4375 prev_prio=118 prev_state=S ==> next_comm=swapper/2 next_pid=0 next_prio=120\n\
					<idle>-0          [001] d.s.  1954.056775: sched_wakeup: comm=kworker/1:1 pid=676 prio=120 success=1 target_cpu=001\n\
					<idle>-0          [001] d...  1954.056804: sched_switch: prev_comm=swapper/1 prev_pid=0 prev_prio=120 prev_state=R ==> next_comm=kworker/1:1 next_pid=676 next_prio=120\n\
					kworker/1:1-676        [001] d...  1954.056838: sched_switch: prev_comm=kworker/1:1 prev_pid=676 prev_prio=120 prev_state=S ==> next_comm=swapper/1 next_pid=0 next_prio=120\n\
					<idle>-0          [000] d.h.  1954.058770: sched_wakeup: comm=DrmEventThread pid=2219 prio=111 success=1 target_cpu=000\n\
					'''

			result['tag'] = ''
		elif result['function'] == 'sched_wakeup':
			for i in range(4, len(tokens) ):
				if tokens[i] == '==>' : continue
				if tokens[i].find('=') < 0: continue

				(k,v) = tokens[i].split('=',2)

				if k == 'comm' : result['cur_comm'] = v
				if k == 'pid'  : result['cur_pid']  = int(v)
				if k == 'prio' : result['cur_prio'] = v
				if k == 'success'   : result['success'] = v
				if k == 'target_cpu': result['target_cpu'] = v

			result['tag'] = ''
		else:
			# skip unknown log
			result['tag'] = ''

		return result

	# parse data from self.file_path into self.result
	def parse_file(self, file_path):
		self.results = []
		self.file_path = file_path
		f = file(self.file_path)
		if f :

			found_head_tag = False
			linenum = 0
			lineorder = 0

			while True:
				line = f.readline()

				# end of file
				if len(line) == 0:
					break

				linenum += 1

				line = line.strip()
				line = line.rstrip('\\n\\')

				# alread run into log, parse log line by line
				if found_head_tag == True :
					# skip comments
					if line.startswith("#"):
						if line.find('TGID') != -1:
							self.__is_support_tgid = True

						continue

					# run into end of perf data lines
					if line.startswith('\\n";'):
						break

					# container for a line of perf data
					log = {
							'task'  : '',
							'pid'   : '',
							'tgid'  : '',

							'cpu'           : '',
							#cpu-'irqs-off'      : '',
							#cpu-'need-resched'  : '',
							#cpu-'hard/softirq'  : '',
							#cpu-'preempt-depth' : '',

							'timestamp' : 0,
							'function'  : '',

							#B(Begin), E(End), P(?), C(?)
							'tag'     : 0,


							#for sched_switch
							'prev_comm' : '',
							'prev_pid'  : -1,
							'prev_prio' : '',
							'prev_state': '',
							'next_comm' : '',
							'next_pid'  : -1,
							'next_prio' : '',

							#for sched_wakeup
							'cur_comm'  : '',
							'cur_pid'   : -1,
							'cur_prio'  : '',
							'success'   : '',
							'target_cpu': '',


							#for tracemark
							'thread'    : -1,
							'event'     : '',


							# for debug
							'raw'   : line,
							'lineno': linenum,

							#index of its Begin/End line
							'refer' : -1,

							#event duration
							'duration'  : 0,
							}

					lineorder += 1
					#try:
					result = self._parse_line(log)
					if result :
						self.results.append ( result )
					elif False == line.endswith('\\n\\'):
						break


				# find head of systrace/MVP log
				if found_head_tag == False and line.startswith("var linuxPerfData = ") :
					found_head_tag = True

			f.close()

		return self.results

	# pair lines of B(Begin) and E(End)
	def post_process(self):
		reviewed = {}
		i = -1

		# put items of 'B' in a bucket of different key(task, pid, function)
		# then items of 'E' pick up its counterpart from bucket
		for r in self.results:
			i += 1
			key = r['task'] + '-' + r['pid'] + '-' + r['function']
			b = None
			if r['tag'] == 'B':
				# put item of 'B' in a proper bucket
				if reviewed.has_key( key ):
					reviewed[key].append( r )
				else:
					reviewed[key] = [r]
			elif r['tag'] == 'E':
				# get the closest item of 'B' from bucket of key(task, pid, function)
				if reviewed.has_key( key ) and len( reviewed[key] ) > 0 :
					b = reviewed[key].pop()

					# set utilities values
					r['refer'] = b['lineno']
					b['refer'] = r['lineno']
					b['duration'] = r['duration'] = r['timestamp'] - b['timestamp']
					r['thread'] = b['thread']
					r['event'] = b['event']

			else:
				#for other tags('P','C',''), do nothing
				pass

		'''
		print reviewed
		for key in reviewed:
			print key
			for line in reviewed[key]:
				print '\t', line['raw']
		'''

		return self.results

	def get_results(self):
		return self.results

	def get_db_conn(self):
		return self.db_conn

	def get_db_cursor(self):
		return self.db_cursor

	# store parse results in sqlite(memory|file)
	def store_results_in_db(self, db):
		self.db_conn = cx = sqlite3.connect(db)
		self.db_cursor = cu = cx.cursor()
		cu.execute('drop table if exists log')
		sql = ''

		cu.execute(''' create table log (_id integer primary key,
						  task varchar(100) default '',
						  pid  integer default -1,
						  tgid integer default -1,
						  cpu  integer default -1,
						  timestamp int default 0,
						  function varchar(100) default '',
						  tag varchar(50) default '',

						  prev_comm varchar(50) default '',
						  prev_pid integer default -1,
						  prev_prio varchar(50) default '',
						  prev_state varchar(50) default '',
						  next_comm varchar(50) default '',
						  next_pid integer default -1,
						  next_prio varchar(50) default '',

						  cur_comm varchar(50) default '',
						  cur_pid integer default -1,
						  cur_prio varchar(50) default '',
						  success varchar(50) default '',
						  target_cpu varchar(50) default '',

						  thread integer default -1,
						  event varchar(100) default '',
						  duration integer,
						  lineno integer,
						  refer  integer
						  ) ''' )
		sql = '''INSERT INTO log
					(_id, task, pid, tgid, cpu, timestamp, function, tag,
							prev_comm, prev_pid, prev_prio, prev_state, next_comm, next_pid, next_prio,
							cur_comm, cur_pid, cur_prio, success, target_cpu,
							thread, event,
							duration, lineno, refer )
					VALUES (?, ?, ?, ?, ?, ?, ?, ?,  ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,  ?, ?, ?, ?, ?, ?) '''

		for r in self.results:
			p = (r['lineno'], r['task'], r['pid'], r['tgid'], r['cpu'], r['timestamp'], r['function'], r['tag'],
					r['prev_comm'], r['prev_pid'], r['prev_prio'], r['prev_state'], r['next_comm'], r['next_pid'], r['next_prio'], # sched_switch
					r['cur_comm'],  r['cur_pid'],  r['cur_prio'],  r['success'],  r['target_cpu'], # sched_wakeup
					r['thread'], r['event'],  # tracemark
					r['duration'],
					#r['raw'],
					r['lineno'], r['refer'] )
			cu.execute( sql, p )

		cx.commit()

'''
Engine will run processors to analyze data from db, then render template with analyzed result
'''
class Engine:
	def __init__(self, db, db_cursor, outfile, is_support_tgid):
		self.db = db
		self.db_cursor = db_cursor
		self.outfile = outfile
		self.processors = []
		self.fp = 0

		self.is_support_tgid = is_support_tgid

	# add processors to analyze data from db,
	# processor is a function, with two parameters( cursor, stash)
	#     cursor : it's a sqlite cursor, it provide data
	def add_processor(self, p):
		self.processors.append(p)

	def process(self):
		# open sqlite db
		if self.db_cursor:
			cx = 0
			cu = self.db_cursor
		else:
			cx = sqlite3.connect(self.db)
			cu = cx.cursor()

		if(DEBUG_ENABLED):
			print 'debug - out file is: ', self.outfile

		# clean outfile
		self.fp = file(self.outfile, 'wb')

		writer = csv.writer(self.fp)
		writer.writerow([])
		writer.writerow(['-'*50])
		writer.writerow(['Timestamp: '+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))])
		writer.writerow(['Execution Time: ' + str("%.2f" % float(get_duration(cu)/1000.0))])
		writer.writerow(['-'*50])
		writer.writerow([])

		try:
			# run processors to analyze data from db
			for p in self.processors:
				if DEBUG_PERF_ENABLED:
					print "Process begin: ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

				p(cu, self.fp, self.is_support_tgid)

				if DEBUG_PERF_ENABLED:
					print "Process end: ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
		except :
			print  sys.exc_info()
		finally:
			if(cu):
				cu.close()
			if(cx):
				cx.close()
			self.fp.close()

def get_task_info(cursor, pid, is_support_tgid):
	ret = {}

	ret['pid'] = pid
	ret['task'] = ''
	ret['tgid'] = 0
	ret['tgtask'] = ''

	if is_support_tgid:
		cursor.execute(''' SELECT task, pid, tgid FROM log WHERE function = 'sched_switch' AND pid = ('%d')  ''' % pid)
		sched_switch_logs = cursor.fetchone()
		if sched_switch_logs:
			ret['task'] = sched_switch_logs[0]
			ret['tgid'] = sched_switch_logs[2]

			if(ret['pid'] == ret['tgid']) or (ret['pid'] == 0):
				ret['tgtask'] = ret['task']
				return ret

			cursor.execute(''' SELECT task, pid, tgid FROM log WHERE function = 'sched_switch' AND pid = ('%d')  ''' % ret['tgid'])
			sched_switch_logs = cursor.fetchone()
			if not sched_switch_logs:
				return ret

			ret['tgtask'] = sched_switch_logs[0]

			return ret
		else:
			cursor.execute(''' SELECT task, pid, tgid FROM log WHERE pid = ('%d')  ''' % pid)
			logs = cursor.fetchone()
			if logs:
				ret['task'] = logs[0]
				ret['tgid'] = logs[2]

			cursor.execute(''' SELECT task, pid, tgid FROM log WHERE pid = ('%d')  ''' % ret['tgid'])
			logs = cursor.fetchone()
			if logs:
				ret['tgtask'] = logs[0]
			else:
				ret['tgtask'] = 'Process-'+str(ret['tgtask'])

			return ret
	else:
		cursor.execute(''' SELECT task, pid, thread, lineno FROM log WHERE function = 'tracing_mark_write' And refer != -1 AND pid = ('%d')  ''' % pid)
		logs = cursor.fetchone()
		if logs:
			ret['task'] = logs[0]
			ret['tgid'] = logs[2]
		else:
			cursor.execute(''' SELECT task, pid, tgid FROM log WHERE function = 'sched_switch' AND pid = ('%d')  ''' % pid)
			logs = cursor.fetchone()
			if logs:
				ret['task'] = logs[0]

		if ret['tgid'] != 0:
			cursor.execute(''' SELECT task, pid, tgid FROM log WHERE function = 'sched_switch' AND pid = ('%d')  ''' % ret['tgid'])
			logs = cursor.fetchone()
			if logs:
				ret['tgtask'] = logs[0]

		return ret

def get_surfaceflinger_info(cursor):
	ret={}

	ret['pid']=None
	ret['task']=None
	ret['tgid']=None
	ret['tgtask']=None

	cursor.execute(''' SELECT task,pid,tgid,event FROM log WHERE event='postFramebuffer' ''')
	logs=cursor.fetchone()
	if logs==None or len(logs)==0:
		return ret

	ret['pid']=logs[1]
	ret['tgid']=logs[2]

	return ret

# processor to calculate the test duration
def get_duration(cursor):
	cursor.execute('SELECT ( MAX(timestamp) - MIN(timestamp) ) AS total_duration FROM log')
	row = cursor.fetchone()

	return row[0] / 1000.0

# processor to calculate fps
def process_fps(cursor, fp, is_support_tgid):
	tracing_result = []

	writer = csv.writer(fp)

	cursor.execute('''SELECT task, pid, tgid, timestamp, event, duration, refer, thread FROM log WHERE (task = 'MFX Engine' OR task = 'Render Engine' OR event LIKE '%EndPicture%' OR event = 'queueBuffer' OR event = 'postFramebuffer' ) AND tag ='B' ORDER BY _id ASC''')
	tracing_mark_logs = cursor.fetchall()
	if tracing_mark_logs == None or len(tracing_mark_logs) == 0 :
		return

	sf_info=get_surfaceflinger_info(cursor)
	for line in tracing_mark_logs:
		if	line[0] == 'MFX Engine' or line[0] == 'Render Engine':
			pid = (int)((str(line[4]).split(':'))[1])
			isGT = 'GT-' + line[0]
		else:
			pid = line[1]
			isGT = 'CPU'

		tracing = filter(lambda x:x['event']==line[4] and x['pid']==pid, tracing_result)
		if not tracing:
			task_info = get_task_info(cursor, pid, is_support_tgid)

			tracing_result.append({
				'event':line[4],
				'pid':task_info['pid'],
				'task':task_info['task'],
				'tgid':task_info['tgid'],
				'tgtask':task_info['tgtask'],
				'duration':0,
				'occurrences':0,
				'max duration':0,
				'min duration':line[5],
				'isGT': isGT,
				'first timestamp': line[3],
				'last timestamp': 0,
				'unmatch number': 0,
				})
			tracing = filter(lambda x:x['event']==line[4] and x['pid']==pid, tracing_result)

		tracing[0]['last timestamp'] = line[3]
		if line[6] != -1:
			tracing[0]['duration'] += line[5]
			tracing[0]['occurrences'] += 1

			if(line[5] > tracing[0]['max duration']):
				tracing[0]['max duration'] = line[5]
			elif(line[5] < tracing[0]['min duration']):
				tracing[0]['min duration'] = line[5]
		else:
			tracing[0]['unmatch number'] += 1

		if'queueBuffer'==line[4] and sf_info['pid']!=line[1]:
			tracing_queueBuffer=filter(lambda x:x['event']=='queueBuffer-all' and x['tgid']==line[-1],tracing_result)
			if not tracing_queueBuffer:
				task_info=get_task_info(cursor,pid, is_support_tgid)
				tracing_result.append({
					'event':'queueBuffer-all',
					'pid':task_info['tgid'],
					'task':None,
					'tgid':task_info['tgid'],
					'tgtask':task_info['tgtask'],
					'duration':0,
					'occurrences':0,
					'max duration':0,
					'min duration':line[5],
					'isGT':isGT,
					'first timestamp':line[3],
					'last timestamp':0,
					'unmatch number':0,
					})
				tracing_queueBuffer=filter(lambda x:x['event']=='queueBuffer-all' and x['tgid']==line[-1],tracing_result)

			tracing_queueBuffer[0]['last timestamp']=line[3]
			if line[6]!=-1:
				tracing_queueBuffer[0]['duration']+=line[5]
				tracing_queueBuffer[0]['occurrences']+=1

				if(line[5]>tracing_queueBuffer[0]['max duration']):
					tracing_queueBuffer[0]['max duration']=line[5]
				elif(line[5]<tracing_queueBuffer[0]['min duration']):
					tracing_queueBuffer[0]['min duration']=line[5]
			else:
				tracing_queueBuffer[0]['unmatch number']+=1

	writer.writerow([])
	writer.writerow(['-'*50])
	writer.writerow(['FPS Info:'])
	writer.writerow(['-'*50])
	writer.writerow([
		'Name',
		'Execution Times(ms)',
		'Occurrences',
		'Avg Duration(ms)',
		'Max Duration(ms)',
		'Min Duration(ms)',
		'Frequency',
		'PID',
		'Thread',
		#'Process PID',
		'Process',
		'IA/GT',
		])
	writer.writerow(['-'*50])

	tracing_result.sort(key=operator.itemgetter('isGT', 'tgid', 'pid', 'event'))

	for line in tracing_result:
		writer.writerow([
			line['event'],
			line['duration'] / 1000.0,
			line['occurrences'],
			line['duration'] / line['occurrences'] / 1000.0,
			line['max duration']/1000.0,
			line['min duration']/1000.0,
			"%.3f" % float((line['occurrences'] + line['unmatch number'] - 1) * 1000.0 * 1000.0 / (line['last timestamp'] - line['first timestamp'])) if (line['occurrences'] + line['unmatch number'] - 1) != 0 else None,
			line['pid'],
			line['task'],
			#line['tgid'],
			line['tgtask'],
			line['isGT'],
			])

	writer.writerow(['-'*50])
	writer.writerow([])

# processor to calculate cpu residency
def process_cpu_residency(cursor, fp, is_support_tgid):
	thread_residency_result = []
	core_residency_result = []
	task_residency_result = []

	writer = csv.writer(fp)

	cursor.execute(''' SELECT task, pid, tgid, cpu, timestamp, prev_comm, prev_pid, next_comm, next_pid FROM log WHERE function = 'sched_switch' ''')
	sched_switch_logs = cursor.fetchall()
	if sched_switch_logs == None or len(sched_switch_logs) == 0 :
		return

	if(DEBUG_ENABLED):
		print 'debug - sched_switch_logs: '
		for line in sched_switch_logs :
			print '\t', line

	all_times = get_duration(cursor)

	unmatched_logs = []
	for line in sched_switch_logs :
		#fine the event on the same cpu
		previous = filter(lambda x:x[3]==line[3], unmatched_logs)
		if previous:
			if(previous[0][8] == line[6]):
				residency_item = filter(lambda x:x['pid']==line[6] and x['cpu']==line[3], thread_residency_result)

				if not residency_item:
					thread_residency_result.append({'task':line[0], 'pid':line[1], 'tgid':line[2], 'cpu':line[3], 'duration':0, 'occurrences':0})
					residency_item = filter(lambda x:x['pid']==line[6] and x['cpu']==line[3], thread_residency_result)

				residency_item[0]['duration'] += line[4] - previous[0][4]
				residency_item[0]['occurrences'] += 1

				if(DEBUG_ENABLED):
					print 'debug - task sched result: '
					print '\t', 'task: ', line[0]
					print '\t', 'cpu: ', line[3]
					print '\t', 'start: ', previous[0][4]
					print '\t', 'duration: ', line[4] - previous[0][4]

			else:
				print 'Error sched_switch LOG: '
				print '\t', previous[0]
				print '\t', line

			unmatched_logs.remove(previous[0])

		unmatched_logs.append(line)

	if(DEBUG_ENABLED):
		print 'debug - task execution parse unmatched logs: '
		for line in unmatched_logs:
			print '\t', line

	'''
	if(DEBUG_ENABLED):
		print 'task execution result: '
		for line in residency_result:
			print line
	'''

	#core
	for line in thread_residency_result:
		#skip idle
		if(line['pid']==0):
			#print 'skip - ', line
			continue

		core = filter(lambda x:x['cpu']==line['cpu'], core_residency_result)
		if not core:
			core_residency_result.append({'cpu':line['cpu'], 'duration':0, 'occurrences':0})
			core = filter(lambda x:x['cpu']==line['cpu'], core_residency_result)

		core[0]['duration'] += line['duration']
		core[0]['occurrences'] += line['occurrences']

		all_cores = filter(lambda x:x['cpu']=='all', core_residency_result)
		if not all_cores:
			core_residency_result.append({'cpu':'all', 'duration':0, 'occurrences':0})
			all_cores = filter(lambda x:x['cpu']=='all', core_residency_result)

		all_cores[0]['duration'] += line['duration']
		all_cores[0]['occurrences'] += line['occurrences']

	core_residency_result.sort(key=operator.itemgetter('cpu'))

	writer.writerow([])
	writer.writerow(['-'*50])
	writer.writerow(['Core Residency/Wakeups Info:'])
	writer.writerow(['-'*50])
	writer.writerow([
		'Core',
		'Execution Times(ms)',
		'Wakeups',
		'Residency'
		])
	writer.writerow(['-'*50])
	for line in core_residency_result:
		writer.writerow([
			line['cpu'],
			line['duration']/1000.0,
			("%.2f" % (line['occurrences'] * 1000.0 / all_times )) +'/s',
			("%.2f" % (line['duration']  * 100.0 / 1000.0 / all_times)) +'%',
			])

	writer.writerow(['-'*50])
	writer.writerow([])

	#task
	for line in thread_residency_result:
		#skip idle
		if(line['pid']==0):
			continue

		tgtask = filter(lambda x:x['tgid']==line['tgid'], task_residency_result)
		if not tgtask:
			tgtask_log = filter(lambda x:x['pid']==line['tgid'], thread_residency_result)

			if(DEBUG_ENABLED):
				if not tgtask_log:
					print 'debug - no tgtask name: ', line

			task_residency_result.append({
				'tgtask': tgtask_log[0]['task'] if tgtask_log else 'noname',
				'tgid':line['tgid'],
				'duration':0,
				'occurrences':0,
				'tasks':[{'task':line['task'], 'pid':line['pid'], 'duration':0,'occurrences':0}]
				})

			tgtask = filter(lambda x:x['tgid']==line['tgid'], task_residency_result)

		tgtask[0]['duration'] += line['duration']
		tgtask[0]['occurrences'] += line['occurrences']

		task = filter(lambda x:x['pid']==line['pid'], tgtask[0]['tasks'])
		if not task:
			tgtask[0]['tasks'].append({
				'task': line['task'],
				'pid':line['pid'],
				'duration':0,
				'occurrences':0,
				})
			task = filter(lambda x:x['pid']==line['pid'], tgtask[0]['tasks'])

		task[0]['duration'] += line['duration']
		task[0]['occurrences'] += line['occurrences']

	task_residency_result.sort(key=operator.itemgetter('duration'), reverse=True)

	writer.writerow([])
	writer.writerow(['-'*50])
	writer.writerow(['Process Residency/Wakups Info:'])
	writer.writerow(['-'*50])
	writer.writerow([
		'Process',
		'Thread',
		'Pid',
		'Wakeups',
		'Residency',
		'Execution Times(ms)',
		])
	writer.writerow(['-'*50])
	for line in task_residency_result:
		writer.writerow([
			line['tgtask'],
			'',
			line['tgid'],
			("%.2f" % float(line['occurrences'] * 1000.0 / all_times)) +'/s',
			("%.2f" % float(line['duration'] * 100.0 / all_times / 1000.0)) +'%',
			("%.2f" % float(line['duration'] / 1000.0)),
			])

		writer.writerow([])
		#print line['tgtask'], line['tgid'], line['duration'],line['occurrences']

		line['tasks'].sort(key=operator.itemgetter('duration'), reverse=True)
		for line1 in line['tasks']:
			writer.writerow([
				'',
				line1['task'],
				line1['pid'],
				("%.2f" % float(line1['occurrences'] * 1000.0 / all_times)) +'/s',
				("%.2f" % float(line1['duration'] * 100.0 / all_times / 1000.0)) +'%',
				("%.2f" % float(line1['duration'] / 1000.0))
				])
		writer.writerow([])

	writer.writerow(['-'*50])
	writer.writerow([])

# processor to calculate gpu residency and fps
def process_gpu_residency(cursor, fp, is_support_tgid ):
	engine_result = []

	writer = csv.writer(fp)

	cursor.execute('''SELECT task, timestamp, event, duration, refer FROM log WHERE (task = 'MFX Engine' OR task = 'Render Engine') AND tag ='B' ORDER BY _id ASC''')
	gt_event_logs = cursor.fetchall()
	if gt_event_logs == None or len(gt_event_logs) == 0 :
		return

	for line in gt_event_logs :
		pid = (int)((str(line[2]).split(':'))[1])

		engine = filter(lambda x:x['engine']==line[0], engine_result)
		if not engine:
			task_info = get_task_info(cursor, pid, is_support_tgid)
			engine_result.append({
				'engine':line[0],
				'duration':0,
				'occurrences':0,
				'events':[{
						'perftag':line[2],
						'pid':task_info['pid'],
						'task':task_info['task'],
						'tgid':task_info['tgid'],
						'tgtask':task_info['tgtask'],
						'max duration':0,
						'min duration':line[3],
						'duration':0,
						'occurrences':0,

						'first timestamp': line[1],
						'last timestamp': 0,
						'unmatch number': 0,
						}]
				})
			engine = filter(lambda x:x['engine']==line[0], engine_result)

		if line[4] != -1:
			engine[0]['duration'] += line[3]
			engine[0]['occurrences'] += 1

		workload = filter(lambda x:x['perftag']==line[2] , engine[0]['events'])
		if not workload:
			task_info = get_task_info(cursor, pid, is_support_tgid)
			engine[0]['events'].append({
						'perftag':line[2],
						'pid':task_info['pid'],
						'task':task_info['task'],
						'tgid':task_info['tgid'],
						'tgtask':task_info['tgtask'],
						'max duration':0,
						'min duration':line[3],
						'duration':0,
						'occurrences':0,

						'first timestamp': line[1],
						'last timestamp': 0,
						'unmatch number': 0,
						})
			workload = filter(lambda x:x['perftag']==line[2] , engine[0]['events'])

		workload[0]['last timestamp'] = line[1]

		if line[4] != -1:
			workload[0]['duration'] += line[3]
			workload[0]['occurrences'] += 1

			if(line[3] > workload[0]['max duration']):
				workload[0]['max duration'] = line[3]
			elif(line[3] < workload[0]['min duration']):
				workload[0]['min duration'] = line[3]
		else:
			workload[0]['unmatch number'] += 1

	#
	writer.writerow([])
	writer.writerow(['-'*50])
	writer.writerow(['GT Residency/Wakups Info:'])
	writer.writerow(['-'*50])
	writer.writerow([
		'Engine',
		'Execution Times(ms)',
		'Occurrences',
		'Residency',

		'Perftag',
		'Avg Duration(ms)',
		'Max Duration(ms)',
		'Min Duration(ms)',
		'Frequency',
		'PID',
		'Thread',
		#'Process PID',
		'Process'
		])
	writer.writerow(['-'*50])

	all_times = get_duration(cursor)
	engine_result.sort(key=operator.itemgetter('engine'), reverse=True)
	for line in engine_result:
		writer.writerow([
			line['engine'],
			line['duration']/1000.0,
			line['occurrences'],
			("%.2f" % float(line['duration']  * 100.0 / all_times / 1000.0)) +'%',

			'',
			'',
			'',
			'',
			'',
			'',
			'',
			#'',
			''
			])
		writer.writerow([])
		line['events'].sort(key=operator.itemgetter('duration'), reverse=True)
		for line1 in line['events']:
			writer.writerow([
				'',
				line1['duration']/1000.0,
				line1['occurrences'],
				("%.2f" % float(line1['duration'] * 100.0 / all_times / 1000.0)) +'%',

				line1['perftag'],
				line1['duration']/(line1['occurrences'])/1000.0,
				line1['max duration']/1000.0,
				line1['min duration']/1000.0,
				"%.3f" % float((line1['occurrences'] + line1['unmatch number'] - 1) * 1000.0 * 1000.0 / (line1['last timestamp'] - line1['first timestamp'])) if (line1['last timestamp'] - line1['first timestamp']) != 0 else None,
				line1['pid'],
				line1['task'],
				#line1['tgid'],
				line1['tgtask']
				])
		writer.writerow([])

	writer.writerow(['-'*50])
	writer.writerow([])

def PrintUsage():
	print "  Usage: " + sys.argv[0] + "  [options]  /path/to/systrace/file"
	print "      -h"
	print "          help"
	#print "      -d"
	#print "          debug"
	#print "      -p"
	#print "          debug performance"
	#print "      -s"
	#print "          sqlite database output"
	print "      -o"
	print "          output file name, default is result.csv"
	sys.exit(1)

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

	if DEBUG_PERF_ENABLED:
		print 'Begin', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

	if(len(output_file) == 0):
		output_file = 'result' + ".csv"

	input_file = arguments[0]

	if(DB_ENABLED):
		db_file = os.path.basename(input_file)+".sqlite"
	else:
		db_file = ':memory:'

	# parse raw data from html file
	parser = Parser()

	if DEBUG_PERF_ENABLED:
		print "parse_file begin: ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

	parser.parse_file(input_file)

	if DEBUG_PERF_ENABLED:
		print "parse_file end: ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

	if DEBUG_PERF_ENABLED:
		print "post_process begin: ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

	parser.post_process()

	if DEBUG_PERF_ENABLED:
		print "post_process end: ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

	if DEBUG_PERF_ENABLED:
		print "store_results_in_db begin: ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

	parser.store_results_in_db(db_file)

	if DEBUG_PERF_ENABLED:
		print "store_results_in_db end: ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))

	# search data from sqlite db file and generate a report
	engine = Engine(db_file, parser.get_db_cursor(), output_file, parser.is_support_tgid())

	engine.add_processor(process_fps)
	engine.add_processor(process_cpu_residency)
	engine.add_processor(process_gpu_residency)

	engine.process()

	if DEBUG_PERF_ENABLED:
		print "End", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
