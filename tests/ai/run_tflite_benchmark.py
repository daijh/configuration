#!/usr/bin/python3 -u

import sys
import os
import re
import pathlib
import subprocess
import argparse
import shutil

# local modules
import pm_shell
import pm_video
from pm_shell import run_shell as run_shell


def main() -> int:
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument('-m',
                        '--model',
                        dest='model',
                        action='store',
                        default='',
                        help="Specify tflite model")
    parser.add_argument('-o',
                        '--output',
                        dest='output',
                        action='store',
                        default='tflite_benchmark_output',
                        help="Specify output")
    args = parser.parse_args()

    # run
    program = './benchmark_model-gpu'
    tflite_model = args.model
    num_runs = 30000

    cmd = f'{program} --graph={tflite_model} --use_gpu=true --run_frequency=30 --num_runs={num_runs}'
    run_shell(cmd, check=False)

    return 0


if __name__ == '__main__':
    sys.exit(main())
