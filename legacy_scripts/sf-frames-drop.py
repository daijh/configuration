#!/usr/bin/python -E

import sys
import os
import re

def getSfPid(traceFile):
    pid = None

    for line in traceFile:
        if re.search('tracing_mark_write.*B\|.*\|postFramebuffer', line):
            pid = re.sub(
                ".*tracing_mark_write.*B\|(?P<pid>[0-9]+)\|postFramebuffer.*", "\g<pid>", line).strip()
            break

    traceFile.seek(0, os.SEEK_SET)
    return pid

def getCount(line):
    return re.sub('.*tracing_mark_write.*C\|.*\|.*\|(?P<count>[0-9]+).*', '\g<count>', line)

def gettimestamp(line):
    pass

if __name__ == '__main__':
    if(len(sys.argv) != 2):
        print 'Usage: ', sys.argv[0], "systrace.html"
        sys.exit(1)

    if not os.path.isfile(sys.argv[1]):
        print "Error: fils does not exist, " + sys.argv[1]
        sys.exit(1)

    path = sys.argv[1]
    traceFile = file(path)

    pid = getSfPid(traceFile)
    p = 'tracing_mark_write.*C\|' + pid + '\|SurfaceView'

    last = None
    lastLine = None
    dropFrame = 0
    for line in traceFile:
        if re.search(p, line):
            count = getCount(line)
            
            if last != None:
                diff = int(last) - int(count)
                if diff > 1:
                    dropFrame += 1

                    print 'drop'
                    print lastLine,
                    print line
            
            last = count
            lastLine = line

    print 'Total Drop Frames: ', dropFrame

