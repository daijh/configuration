#!/usr/bin/python3 -u

import sys
import os
import re
import pathlib
import subprocess
import argparse
import shutil

# local modules
from pm_shell import exec_bash as exec_bash


def trace_header(input, output):
    cmd = f'ffmpeg -i {input} -vcodec copy -bsf:v trace_headers -f null - '
    exec_bash(cmd, log_file=output)

    return


def video_frames(trace_header) -> int:
    frames = 0

    with open(f'{trace_header}', 'r', encoding="utf-8") as trace_file:
        for line in trace_file:
            m = re.match(r"^frame=\s+(?P<frames>[0-9]+)\s+.*", line)
            # The pattern matches multiple times, and we need the last match.
            if m:
                frames = m.group('frames')

    return frames
