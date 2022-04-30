#!/usr/bin/python -E

import sys
import os
import re

import sqlite3

def parse_bo_leftovers(cursor):
	cursor.execute('SELECT SUM(memDelta) FROM bo_leftovers')
	bo_sum = cursor.fetchone()

	cursor.execute('select SUM(memDelta), COUNT(*), memDelta, callName, boName, trace FROM bo_leftovers GROUP BY trace ORDER BY SUM(memDelta) DESC')

	db_result = cursor.fetchall()

	result = []
	result.append("===============Bo Size Sum is " + str(bo_sum[0]) + " Byte\n")
	result.append("Total Bo Size\t\t\tCall Count\t\t\tBo Size\t\t\tBo Name\t\t\tCallStack\n")

	for line in db_result:
		result.append(str(line[0])+"\t\t\t"+str(line[1])+"\t\t\t"+str(line[2])+"\t\t\t"+str(line[4])+"\t\t\t"+str(line[5])+"\n")

	return result

def parse_bo_leftovers_component(cursor, name):
	cursor.execute('select SUM(memDelta), COUNT(*), memDelta, callName, boName, trace FROM bo_leftovers GROUP BY trace ORDER BY SUM(memDelta) DESC')
	db_result = cursor.fetchall()

	bo_sum = 0
	for line in db_result:
		if(re.search(name, str(line[5]))):
			bo_sum += line[0]

	result = []
	result.append("===============" + name + " Bo Size Sum is " + str(bo_sum) + " Byte\n")
	result.append("Total Bo Size\t\t\tCall Count\t\t\tBo Size\t\t\tBo Name\t\t\tCallStack\n")

	for line in db_result:
		if(re.search(name, str(line[5]))):
			result.append(str(line[0])+"\t\t\t"+str(line[1])+"\t\t\t"+str(line[2])+"\t\t\t"+str(line[4])+"\t\t\t"+str(line[5])+"\n")

	return result

def parse_mem_leftovers(cursor):
	cursor.execute('SELECT SUM(memDelta) FROM mem_leftovers')
	mem_sum = cursor.fetchone()

	cursor.execute('SELECT SUM(memDelta), COUNT(*), memDelta, trace FROM mem_leftovers GROUP BY trace ORDER BY SUM(memDelta) DESC')

	db_result = cursor.fetchall()

	result = []
	result.append("===============Mem Size Sum is " + str(mem_sum[0]) + " Byte\n")
	result.append("Total Mem Size\t\t\tCall Count\t\t\tMem Size\t\t\tCallStack\n")

	for line in db_result:
		result.append(str(line[0])+"\t\t\t"+str(line[1])+"\t\t\t"+str(line[2])+"\t\t\t"+str(line[3])+"\n")

	return result

def parse_mem_leftovers_component(cursor, name):
	cursor.execute('SELECT SUM(memDelta), COUNT(*), memDelta, trace FROM mem_leftovers GROUP BY trace ORDER BY SUM(memDelta) DESC')
	db_result = cursor.fetchall()

	mem_sum = 0
	for line in db_result:
		if(re.search(name, str(line[3]))):
			mem_sum += line[0]

	result = []
	result.append("===============" + name + " Mem Size Sum is " + str(mem_sum) + " Byte\n")
	result.append("Total Mem Size\t\t\tCall Count\t\t\tMem Size\t\t\tCallStack\n")

	for line in db_result:
		if(re.search(name, str(line[3]))):
			result.append(str(line[0])+"\t\t\t"+str(line[1])+"\t\t\t"+str(line[2])+"\t\t\t"+str(line[3])+"\n")

	return result

if __name__ == '__main__':
	if(len(sys.argv) != 2):
		print 'Usage: ', sys.argv[0], "db-filename"
		sys.exit(1)

	if not os.path.isfile(sys.argv[1]):
		print "Error: fils does not exist, "+sys.argv[1]
		sys.exit(1)

	conn = sqlite3.connect(sys.argv[1])
	cursor = conn.cursor()

	# Parse Bo Allocation
	bo_leftovers_result=parse_bo_leftovers(cursor)
	CodecHal_bo_leftovers_result = parse_bo_leftovers_component(cursor, 'CodecHal')
	VpHal_bo_leftovers_result = parse_bo_leftovers_component(cursor, 'VpHal')
	CmHal_bo_leftovers_result = parse_bo_leftovers_component(cursor, 'HalCm')
	Surface_bo_leftovers_result = parse_bo_leftovers_component(cursor, 'vaCreateSurfaces')
	Buffer_bo_leftovers_result = parse_bo_leftovers_component(cursor, 'vaCreateBuffer')
	pavp_bo_leftovers_result = parse_bo_leftovers_component(cursor, 'libpavp')

	# Parse Mem Allocation
	mem_leftovers_result=parse_mem_leftovers(cursor)
	CodecHal_mem_leftovers_result = parse_mem_leftovers_component(cursor, 'CodecHal')
	VpHal_mem_leftovers_result = parse_mem_leftovers_component(cursor, 'VpHal')
	CmHal_mem_leftovers_result = parse_mem_leftovers_component(cursor, 'HalCm')
	pavp_mem_leftovers_result = parse_mem_leftovers_component(cursor, 'libpavp')

	print "==========Summary Bo Allocation\n"
	print bo_leftovers_result[0]
	print CodecHal_bo_leftovers_result[0]
	print VpHal_bo_leftovers_result[0]
	print CmHal_bo_leftovers_result[0]
	print Surface_bo_leftovers_result[0]
	print Buffer_bo_leftovers_result[0]
	print pavp_bo_leftovers_result[0]
	print "==========End\n"
	print "==========Summary Mem Allocation\n"
	print mem_leftovers_result[0]
	print CodecHal_mem_leftovers_result[0]
	print VpHal_mem_leftovers_result[0]
	print CmHal_mem_leftovers_result[0]
	print pavp_mem_leftovers_result[0]
	print "==========End\n"

	print "==========Detail\n"
	for line in bo_leftovers_result:
		print line

	for line in CodecHal_bo_leftovers_result:
		print line

	for line in VpHal_bo_leftovers_result:
		print line

	for line in CmHal_bo_leftovers_result:
		print line

	for line in Surface_bo_leftovers_result:
		print line

	for line in Buffer_bo_leftovers_result:
		print line

	for line in pavp_bo_leftovers_result:
		print line

    #mem
	for line in mem_leftovers_result:
		print line

	for line in CodecHal_mem_leftovers_result:
		print line

	for line in VpHal_mem_leftovers_result:
		print line

	for line in CmHal_mem_leftovers_result:
		print line

	for line in pavp_mem_leftovers_result:
		print line

	# Close
	cursor.close()
	conn.close()
