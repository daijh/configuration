#!/usr/bin/python -E

import getopt
import sys
import os
import string
import re

if __name__ == '__main__':
	if(len(sys.argv) != 2):
		print 'Usage: ', sys.argv[0], "filename"
		sys.exit(1)

	fileobj = open(sys.argv[1], 'r')
	lines = fileobj.readlines()
	fileobj.close()

	filenameMerged='.tmp-mergeCallStack.txt'
	filenameSorted='.tmp-mergeCallStack-sorted.txt'

	mergeCallStackFile = open(filenameMerged, 'w')

	#print contents

	result=''
	match_begin=0
	for line in lines:
		item=line.strip()
		if(re.match(r'^"\d*"', item)):
			if(match_begin):
				#print re.sub('"', '', result)
				mergeCallStackFile.write(re.sub('"', '', result)+"\n");
			result=re.sub(',','|',item)
			match_begin=1
		else:
			if(match_begin):
				result+=item

	if(match_begin):
		#print re.sub('"', '', result)
		mergeCallStackFile.write(re.sub('"', '', result)+"\n");

	mergeCallStackFile.close();

	#sort
	cmd = "sort -t'|' -k 5 -g -r " + filenameMerged + ">" + filenameSorted
	#print cmd
	stream = os.popen(cmd)
	stream.close()

	#process 
	out = []

	cmd = "awk -F\"|\" '{sum+=$5}; END {print \"\\n==========Total Heap Mem Size is:\", sum, \"Bytes==========\\n\"}' " + filenameSorted 
	stream = os.popen(cmd)
	lines = stream.readlines()
	stream.close()
	#print lines

	total_bo_size = []
	total_bo_size.extend(lines)
	#print total_bo_size
	#out = lines;

	cmd = "awk -F\"|\" '/CodecHal/ {sum+=$5; print \"Mem Size: \", $5, \"\\n\", $7, \"\\n\"}; END {print \"\\n==========Total CodecHal Mem Size is:\", sum, \"Bytes==========\\n\"}' " + filenameSorted 
	stream = os.popen(cmd)
	lines = stream.readlines()
	stream.close()

	out.extend(lines[-3:]);
	out.extend(lines[:-3]);
	

	cmd = "awk -F\"|\" '/VpHal/ {sum+=$5; print \"Mem Size: \", $5, \"\\n\", $7, \"\\n\"}; END {print \"\\n==========Total VpHal Mem Size is:\", sum, \"Bytes==========\\n\"}' " + filenameSorted 
	stream = os.popen(cmd)
	lines = stream.readlines()
	stream.close()
	#for line in lines:
	#	print line
	#print cmd

	#resut += lines;
	out.extend(lines[-3:]);
	out.extend(lines[:-3]);

	cmd = "awk -F\"|\" '/vaCreateSurfaces/ {sum+=$5; print \"Mem Size: \", $5, \"\\n\", $7, \"\\n\"}; END {print \"\\n==========Total vaCreateSurfaces Mem Size is:\", sum, \"Bytes==========\\n\"}' " + filenameSorted 
	stream = os.popen(cmd)
	lines = stream.readlines()
	stream.close()
	#for line in lines:
	#	print line
	#print cmd

	#resut += lines;
	out.extend(lines[-3:]);
	out.extend(lines[:-3]);

	cmd = "awk -F\"|\" '/vaCreateBuffer/ {sum+=$5; print \"Mem Size: \", $5, \"\\n\", $7, \"\\n\"}; END {print \"\\n==========Total vaCreateBuffer Mem Size is:\", sum, \"Bytes==========\\n\"}' " + filenameSorted 
	stream = os.popen(cmd)
	lines = stream.readlines()
	stream.close()
	#for line in lines:
	#	print line
	#print cmd

	#resut += lines;
	out.extend(lines[-3:]);
	out.extend(lines[:-3]);

	cmd = "grep -E -v 'CodecHal|VpHal|vaCreateSurfaces|vaCreateBuffer' " +  filenameSorted + "|" + "awk -F\"|\" '{sum+=$5; print \"Mem Size: \", $5, \"\\n\", $7, \"\\n\"}; END {print \"\\n==========Total Other Mem Size is:\", sum, \"Bytes==========\\n\"}' "
	#print cmd
	stream = os.popen(cmd)
	lines = stream.readlines()
	stream.close()
	#for line in lines:
	#	print line

	#resut += lines;
	out.extend(lines[-3:]);
	out.extend(lines[:-3]);

	#for line in out:
	#	print line

	#summary
	#summary=[]
	outPutName='mem_leftovers-output.txt'
	outFile = open(outPutName, 'w')

	outFile.write("Summary:\n")
	for line in total_bo_size:
		outFile.write(line)

	for line in out:
		#print line
		if(re.match(r'===', line)):
			outFile.write("\t" + line)
			#print line
			#summary.append(line)

	#print summary

	#split

	match_begin=0
	for line in out:
		item=line.strip().split('\\')
		for field in item:
			outFile.write(field + "\n")
			#print field 


	outFile.close()
	print "Result is "+outPutName

