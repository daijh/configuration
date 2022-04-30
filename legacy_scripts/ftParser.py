#! /usr/bin/python

# @author       jianhui.j.dai@intel.com
# @brief
# @version      0.1
# @date         2015/01/23

import os
import sys
import getopt
import operator
import re
import sqlite3


def PrintUsage():
    print ""
    print "  Usage: " + sys.argv[0] + "ftrace_file"
    print "      -h"
    print "          help"
    print "      -i"
    print "          function name"
    print ""
    print "  Sample: "
    print ""
    print "          " + sys.argv[0] + '  -i  drm_prime_handle_to_fd_ioctl  trace.txt'
    print ""
    sys.exit(1)


def main(argv):
    try:
        options, arguments = getopt.getopt(argv[1:], "hi:", [])
    except getopt.GetoptError, error:
        PrintUsage()

    g_input = None
    g_func = '.'

    if len(arguments) != 1:
        PrintUsage()

    g_input = arguments[0]

    for option, value in options:
        if option == "-h":
            PrintUsage()
        elif option == "-i":
            g_func = value
        else:
            PrintUsage()

    if not os.path.exists(g_input):
        print '*' * 10
        print 'Error:', 'Input dose not existed,', os.path.abspath(g_input)
        print '*' * 10
        sys.exit(1)

    records = []
    for line in file(g_input, 'r'):
        if re.search(g_func, line):
            items = line.split()

            if re.search('/\*.*\*/', line):
                tag = 'E'
            else:
                tag = 'B'

            records += [[items[0], tag]]

    totla_duration = 0
    calls = 0
    result = []
    max_duration = 0
    min_duration = 0
    for i in range(len(records)):
        if records[i][1] == 'E' and records[i - 1][1] == 'B' :
            duration = float(records[i][0]) - float(records[i - 1][0])
            result += [[records[i - 1][0], records[i][0], ('%f' % duration)]]

            totla_duration += float(duration)
            calls += 1

            if min_duration == 0 or min_duration > duration:
                min_duration = duration
            if max_duration < duration:
                max_duration = duration


    for i in result:
        print i

    print 'AVG: %f' % (totla_duration / calls)
    print 'MAX: %f' % max_duration 
    print 'MIN: %f' % min_duration 


if __name__ == '__main__':
    main(sys.argv)
