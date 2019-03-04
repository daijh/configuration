#! /usr/bin/python

# @author	jianhui.j.dai@intel.com
# @brief
# @version	0.1
# @date		2019/03/15

import os
import sys
import getopt
import re
import time

def gt_freq():
    '''
    /sys/devices/pci0000:00/0000:00:02.0/drm/card0
    '''

    try:
        gpu_dir='/sys/devices/pci0000:00/0000:00:02.0/drm/card0'

        file=open(gpu_dir + '/gt_max_freq_mhz')
        max_freq=file.readline().strip()
        file.close()

        file=open(gpu_dir + '/gt_min_freq_mhz')
        min_freq=file.readline().strip()
        file.close()

        file=open(gpu_dir + '/gt_act_freq_mhz')
        act_freq=file.readline().strip()
        file.close()

        file=open(gpu_dir + '/gt_cur_freq_mhz')
        cur_freq=file.readline().strip()
        file.close()

        print "gpu max freq: ", max_freq
        print "gpu min freq: ", min_freq
        print "gpu cur freq: ", cur_freq
        print "gpu act freq: ", act_freq
    except Exception as e:
        print e

def ia_freq():
    '''
    /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq
    '''

    cpu_dir='/sys/devices/system/cpu/'
    cpus_filename='possible'
    maxfreq_filename='scaling_max_freq'
    minfreq_filename='scaling_min_freq'
    curfreq_filename='scaling_cur_freq'

    cpus_file=open(cpu_dir + cpus_filename, 'r')
    line = cpus_file.readline().strip()
    cpus_file.close()
    print "cpu: ", line
    cpus = int(re.sub(r'0-([0-9]*)', r'\1', line))

    maxfreq_file = open(cpu_dir + 'cpu0/cpufreq/' + maxfreq_filename, 'r')
    maxfreq=maxfreq_file.readline().strip()
    maxfreq_file.close()

    minfreq_file = open(cpu_dir + 'cpu0/cpufreq/' + minfreq_filename, 'r')
    minfreq=minfreq_file.readline().strip()
    minfreq_file.close()
    print ('min freq: {0},\tmax freq: {1}'.format(minfreq, maxfreq))

    for cpu in range(cpus + 1):
        filename = cpu_dir + 'cpu' + str(cpu) + '/cpufreq/' + curfreq_filename
        file = open(filename, 'r')
        cur_freq = file.readline().strip()
        file.close()

        print('cpu{0:<3}:{1:>10}'.format(cpu, cur_freq)),

        if cpus <= 8:
            print('')
        else:
            if cpu == cpus:
                print('')
            elif (cpu+1) % 8 != 0:
                print(',\t'),
            else:
                print('')

def PrintUsage():
    print "Usage: " + sys.argv[0] + " [] "

    sys.exit(1)

if __name__ == '__main__':

    while True:
        print '*#' * 10
        ia_freq()
        print '--' * 10
        gt_freq()
        print '*#' * 10
        time.sleep(1)

