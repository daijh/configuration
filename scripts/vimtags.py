#! /usr/bin/python

# @author	jianhui.j.dai@intel.com
# @brief
# @version	0.1
# @date		2014/07/03

import os
import sys
import getopt
import re


def doClean():
    cmd = 'find -maxdepth 4 -regextype "posix-egrep" -regex ".*/GPATH|.*/GRTAGS|.*/GTAGS|.*/filenametags|.*/gtags.files" | xargs rm -v'
    os.system(cmd)

    print '*#' * 10
    print 'Delete Tags Done!'
    print '*#' * 10


def doUpdate():
    cmd = 'gtags -i'
    os.system(cmd)

    print '*#' * 10
    print 'Update Tags Done!'
    print '*#' * 10


def genTags(paths):

    cmd = '(echo "!_TAG_FILE_SORTED    2   /2=foldcase/"; (find ' +  ' '.join(paths) + \
        ' \( -name .svn -o -name .repo -o -name .git \) -prune -o -type f -printf "%f\\t%p\\t1\\n" | sort -f)) > ./filenametags;'
    os.system(cmd)

    cmd = 'find ' + ' '.join(paths) + ' -type f -print > gtags.files'
    os.system(cmd)

    cmd = 'gtags -i'
    os.system(cmd)

    print '*#' * 10
    print 'Generate Tags Done!'
    print '*#' * 10


def PrintUsage():
    print "Usage: " + sys.argv[0] + " [-c-u-a] " + " path1 path2 path3 ..."
    print "Options:"
    print "\t-c",
    print "\t" + 'clean'
    print "\t-u",
    print "\t" + 'update'

    sys.exit(1)

if __name__ == '__main__':

    try:
        options, arguments = getopt.getopt(sys.argv[1:], 'cu', [])
    except getopt.GetoptError, error:
        PrintUsage()

    optClean = False
    optUpdate = False
    optPaths = []

    '''
    if len(arguments) == 0:
        print 'null path'
        PrintUsage()
    '''

    optPaths = arguments

    for option, value in options:
        if option == "-c":
            optClean = True
        elif option == "-u":
            optUpdate = True
        else:
            print 'invalid option: ', option
            PrintUsage()

    optPaths = filter(lambda x: os.path.isdir(x), optPaths)
    if len(optPaths) == 0:
        optPaths += ["."]

    if optClean:
        doClean()
        sys.exit(1)

    if optUpdate:
        doUpdate()
        sys.exit(1)

    print optPaths

    genTags(optPaths)
