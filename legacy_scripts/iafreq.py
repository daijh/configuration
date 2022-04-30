#!/usr/bin/python -E

import sys
import os
import re
import time
import getopt

'''
jdai12@lab:/opt/WorkDir/android$ adb shell ls /sys/devices/system/cpu/cpu0/cpufreq/ -l
-r--r--r-- root     root         4096 2014-11-19 02:28 affected_cpus
-r-------- root     root         4096 2014-11-19 02:28 cpuinfo_cur_freq
-r--r--r-- root     root         4096 2014-11-19 02:28 cpuinfo_max_freq
-r--r--r-- root     root         4096 2014-11-19 02:28 cpuinfo_min_freq
-r--r--r-- root     root         4096 2014-11-19 02:28 cpuinfo_transition_latency
-r--r--r-- root     root         4096 2014-11-19 02:28 related_cpus
-r--r--r-- root     root         4096 2014-11-19 02:28 scaling_available_governors
-r--r--r-- root     root         4096 2014-11-19 02:28 scaling_driver
-rw-r--r-- root     root         4096 2014-11-19 06:59 scaling_governor
-rw-rw---- system   system       4096 2014-11-19 02:28 scaling_max_freq
-rw-rw-r-- system   system       4096 2014-11-19 02:28 scaling_min_freq
-rw-r--r-- root     root         4096 2014-11-19 02:28 scaling_setspeed
drwxr-xr-x root     root              2014-11-19 02:28 stats
'''

_CPU_PATH = '/sys/devices/system/cpu'

def get_cpu_info_cur_freq(core):
    cmd = 'adb shell cat ' + _CPU_PATH + '/cpu' + str(core) + '/cpufreq/cpuinfo_cur_freq'
    stream = os.popen(cmd)
    lines = stream.readlines()

    cur_freq = int(lines[0].strip())

    return cur_freq

def get_cpu_info_cur_governor(core):
    cmd = 'adb shell cat ' + _CPU_PATH + '/cpu' + str(core) + '/cpufreq/scaling_governor'
    stream = os.popen(cmd)
    lines = stream.readlines()

    governor = lines[0].strip()

    return governor 

def set_cpu_info_governor_performance(core):
    cmd = 'adb shell "echo performance > ' + _CPU_PATH + '/cpu' + str(core) + '/cpufreq/scaling_governor"'
    stream = os.popen(cmd)
    lines = stream.readlines()

def get_cpu_info_support_freq(core):
    ret = []

    #/sys/devices/system/cpu/cpu0/cpufreq/stats 
    cmd = 'adb shell cat ' + _CPU_PATH + '/cpu' + str(core) + '/cpufreq/stats/time_in_state'
    stream = os.popen(cmd)
    lines = stream.readlines()

    print '\tSupport freq:', 
    for line in lines:
        print line
        ret += line.split()[0]

    print ret
    return ret

def get_cpu_info_cpu_freq_range(core):
    ret = {}

    ret['cpu_min_freq'] = 0
    ret['cpu_max_freq'] = 0

    cmd = 'adb shell cat ' + _CPU_PATH + '/cpu' + str(core) + '/cpufreq/cpuinfo_min_freq'
    stream = os.popen(cmd)
    lines = stream.readlines()

    ret['cpu_min_freq'] = int(lines[0].strip())

    cmd = 'adb shell cat ' + _CPU_PATH + '/cpu' + str(core) + '/cpufreq/cpuinfo_max_freq'
    stream = os.popen(cmd)
    lines = stream.readlines()

    ret['cpu_max_freq'] = int(lines[0].strip())

    return ret

def get_cpu_info_scaling_freq(core):
    ret = {}

    ret['scaling_min_freq'] = 0
    ret['scaling_max_freq'] = 0

    cmd = 'adb shell cat ' + _CPU_PATH + '/cpu' + str(core) + '/cpufreq/scaling_min_freq'
    stream = os.popen(cmd)
    lines = stream.readlines()

    ret['scaling_min_freq'] = int(lines[0].strip())

    cmd = 'adb shell cat ' + _CPU_PATH + '/cpu' + str(core) + '/cpufreq/scaling_max_freq'
    stream = os.popen(cmd)
    lines = stream.readlines()

    ret['scaling_max_freq'] = int(lines[0].strip())

    return ret

def get_cpu_info_available_governor(core):
    ret = []

    cmd = 'adb shell cat ' + _CPU_PATH + '/cpu' + str(core) + '/cpufreq/scaling_available_governors'
    stream = os.popen(cmd)
    lines = stream.readlines()

    for line in lines:
        ret += line.split()

    return ret

def disable_c_state(core):

    cmd = 'adb shell ls ' + _CPU_PATH + '/cpu' + str(core) + '/cpuidle'
    stream = os.popen(cmd)
    lines = stream.readlines()
        
    states = []

    for line in lines:
        if re.match('state[0-9]', line.strip()):
            states += [line.strip()[-1]]

    states.sort()

    for p in states[1:]:
        cmd = 'adb shell "echo 1 > ' + _CPU_PATH + '/cpu' + str(core) + '/cpuidle' + '/state' + p + '/disable"'
        stream = os.popen(cmd)
        lines = stream.readlines()

    return

def PrintUsage():
    print "Usage: " + sys.argv[0] + " [-qsh] "
    print "Options:"
    print "\t-q",
    print "\t" + 'query cur freq' 
    print "\t-s",
    print "\t" + 'set max freq' 
    print "\t-h",
    print "\t" + 'help' 

    sys.exit(1)

if __name__ == '__main__':

    try:
        options, arguments = getopt.getopt(sys.argv[1:], 'qsh', [])
    except getopt.GetoptError, error:
        PrintUsage()

    if len(arguments) != 0 or len(options) == 0:
    	PrintUsage()

    need_set = False 

    for option, value in options:
        if option == "-q":
            pass
        elif option == "-s":
            need_set = True
        elif option == "-h":
            PrintUsage()
        else:
            print 'error'
            PrintUsage()

    cmd = 'adb shell cat /sys/devices/system/cpu/online'
    stream = os.popen(cmd)
    lines = stream.readlines()
    # 0-3

    #print lines
    num_core = int(lines[0].strip()[-1])

    for core in range(num_core + 1):
        print '*******************'
        print 'Core', core, ':'

        ret = get_cpu_info_scaling_freq(core)
        print '\t', 'scaling_min_freq:', ret['scaling_min_freq'], ',', 'scaling_max_freq:', ret['scaling_max_freq']

        ret = get_cpu_info_cpu_freq_range(core)
        print '\t', 'cpu_min_freq:', ret['cpu_min_freq'], ',', 'cpu_max_freq:', ret['cpu_max_freq']

        ret = get_cpu_info_available_governor(core)
        print '\t', 'available_governor:',
        for g in ret:
            print g, 
        print ''

        ret = get_cpu_info_cur_freq(core)
        print '\t', 'cur_freq:', ret

        ret = get_cpu_info_cur_governor(core)
        print '\t', 'cur_governor:', ret
        print '*******************'

    if need_set: 

        # disable p state
        for core in range(num_core + 1):
            print '*******************'
            print 'Core', core, ': disable p state'

            disable_c_state(core)
            print '*******************'

        # set governor to performance
        for core in range(num_core + 1):
            print '*******************'
            print 'Core', core, ': set governor performance'
            set_cpu_info_governor_performance(core)

            ret = get_cpu_info_cur_governor(core)
            print '\t', 'cur_governor:', ret
            print '*******************'

    # query current freq
    while True:
        time.sleep(1)
        print '*******************'
        for core in range(num_core + 1):
            print 'Core', core, ':'
            ret = get_cpu_info_cur_freq(core)
            print '\t', 'cur_freq:', ret
        print '*******************'
