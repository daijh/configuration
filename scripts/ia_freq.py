#!/usr/bin/python3 -E

import sys
import os
import re
import time
import getopt

def PrintUsage():
    print ("Usage: " + sys.argv[0] + " [-sh] ")
    print ("Options:")
    print ("\t-s")
    print ("\t\t" + 'set max freq')
    print ("\t-h")
    print ("\t\t" + 'help')

    sys.exit(1)

if __name__ == '__main__':
    try:
        options, arguments = getopt.getopt(sys.argv[1:], 's:h', [])
    except getopt.GetoptError as error:
        PrintUsage()

    freq = -1;

    for option, value in options:
        if option == "-s":
            freq = value
        elif option == "-h":
            PrintUsage()
        else:
            PrintUsage()

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
    print("cpu: ", line)
    cpus = int(re.sub(r'0-([0-9]*)', r'\1', line))


    if (freq != -1):
        for cpu in range(cpus + 1):
            maxfreq_file = open(cpu_dir + 'cpu' + str(cpu) + '/cpufreq/' + maxfreq_filename, 'r')
            maxfreq=maxfreq_file.readline().strip()
            maxfreq_file.close()

            minfreq_file = open(cpu_dir + 'cpu' + str(cpu) + '/cpufreq/' + minfreq_filename, 'r')
            minfreq=minfreq_file.readline().strip()
            minfreq_file.close()

            if (int(freq) <  int(minfreq)):
                print("Invalid freq " + freq);
                break;

            maxfreq_path = "/sys/devices/system/cpu/cpu" + str(cpu) + "/cpufreq/scaling_max_freq"
            cmd = 'echo ' + str(freq) + ' > ' + maxfreq_path
            stream = os.popen(cmd)
            #print(cmd)
            lines = stream.readlines()

            print("cpu%3d, set max freq %s" % (cpu, freq))

    for cpu in range(cpus + 1):
        maxfreq_file = open(cpu_dir + 'cpu' + str(cpu) + '/cpufreq/' + maxfreq_filename, 'r')
        maxfreq=maxfreq_file.readline().strip()
        maxfreq_file.close()

        minfreq_file = open(cpu_dir + 'cpu' + str(cpu) + '/cpufreq/' + minfreq_filename, 'r')
        minfreq=minfreq_file.readline().strip()
        minfreq_file.close()

        print("cpu%3d, min freq %s, max freq %s" % (cpu, minfreq, maxfreq))

        #print('min freq: {0},\tmax freq: {1}'.format(minfreq, maxfreq))

