#!/usr/bin/python3 -u

import sys
import os
import re
import pathlib
import subprocess
import argparse
import shutil
'''
kernel.org/doc/Documentation/cpu-freq/governors.txt
https://www.kernel.org/doc/Documentation/cpu-freq/governors.txt
'''


def main() -> int:
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument('-m',
                        '--mode',
                        dest='mode',
                        action='store',
                        default='performance',
                        help="Specify CPU mode")
    args = parser.parse_args()

    for i in range(1000):
        cpu_x_path = pathlib.Path(
            f'/sys/devices/system/cpu/cpu{i}/cpufreq/scaling_governor')
        if not cpu_x_path.exists():
            break

        cpu_x_path.write_text(args.mode)
        print(f'Write {cpu_x_path}, {args.mode}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
