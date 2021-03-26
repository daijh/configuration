#!/usr/bin/python3 -E

import sys
import os
import re
import time
import getopt

def PrintUsage():
    print ("Usage: " + sys.argv[0] + " [-edh] ")
    print ("Options:")
    print ("\t-d")
    print ("\t\t" + 'disable p state')
    print ("\t-e")
    print ("\t\t" + 'enable p state')
    print ("\t-h")
    print ("\t\t" + 'help')

    sys.exit(1)

if __name__ == '__main__':
    try:
        options, arguments = getopt.getopt(sys.argv[1:], 'd:e:h', [])
    except getopt.GetoptError as error:
        PrintUsage()

    disable = -1;
    pstate = -1;

    for option, value in options:
        if option == "-e":
            pstate = value
            disable = 0;
        elif option == "-d":
            pstate = value
            disable = 1;
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

    maxfreq_file = open(cpu_dir + 'cpu0/cpufreq/' + maxfreq_filename, 'r')
    maxfreq=maxfreq_file.readline().strip()
    maxfreq_file.close()

    minfreq_file = open(cpu_dir + 'cpu0/cpufreq/' + minfreq_filename, 'r')
    minfreq=minfreq_file.readline().strip()
    minfreq_file.close()
    print('min freq: {0},\tmax freq: {1}'.format(minfreq, maxfreq))

    # p state
    for cpu in range(cpus + 1):
        print ('*******************')
        print ('Core', cpu, ': p state')

        cpuidle_patch = "/sys/devices/system/cpu/cpu" + str(cpu) + "/cpuidle/"

        cmd = 'ls ' + cpuidle_patch
        stream = os.popen(cmd)
        lines = stream.readlines()
        print(lines);
        n_states = len(lines);

        if (disable != -1 and pstate != -1):
            if (int(pstate) < 0 or int(pstate) >= n_states):
                print("Invalid pstate: " + pstate);
                exit();

            # set p0
            cpuidle_state_patch = cpuidle_patch + "state" + pstate + "/disable"
            cmd = 'echo ' + str(disable) + ' > ' + cpuidle_state_patch
            stream = os.popen(cmd)
            print(cmd)
            lines = stream.readlines()

        for state in range(n_states):
            cpuidle_state_patch = cpuidle_patch + "state" + str(state) + "/disable"
            cmd = 'cat ' + cpuidle_state_patch
            stream = os.popen(cmd)
            lines = stream.readlines()

            print("state" + str(state) + ":" + lines[0])
        print ('*******************')

