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
    ref = '/home/webrtc/third_party/test_streams/gipsrestat-1280x720_20210211.vp9-remux-300frames.ivf'

    inputs = []
    base_path = pathlib.Path(
        '/workspace/script_utilities/webrtc/tests/workspace/buf_initial_sz'
    ).resolve()
    inputs.append(
        base_path.joinpath(
            'tests-buf_initial_sz-500/gipsrestat-1280x720_20210211.vp9-remux.ivf/1280x720-framerate30-bitrate1500/output-VP9-L1T3-L0T2.ivf'
        ))
    inputs.append(
        base_path.joinpath(
            'tests-buf_initial_sz-1000/gipsrestat-1280x720_20210211.vp9-remux.ivf/1280x720-framerate30-bitrate1500/output-VP9-L1T3-L0T2.ivf'
        ))
    inputs.append(
        base_path.joinpath(
            'tests-buf_initial_sz-500/gipsrestat-1280x720_20210211.vp9-remux.ivf/1280x720-framerate30-bitrate1500/output-VP9-L1T1-L0T0.ivf'
        ))
    inputs.append(
        base_path.joinpath(
            'tests-buf_initial_sz-1000/gipsrestat-1280x720_20210211.vp9-remux.ivf/1280x720-framerate30-bitrate1500/output-VP9-L1T1-L0T0.ivf'
        ))

    inputs.append(
        base_path.joinpath(
            'tests-buf_initial_sz-500/gipsrestat-1280x720_20210211.vp9-remux.ivf/1280x720-framerate30-bitrate2500/output-VP9-L1T3-L0T2.ivf'
        ))
    inputs.append(
        base_path.joinpath(
            'tests-buf_initial_sz-1000/gipsrestat-1280x720_20210211.vp9-remux.ivf/1280x720-framerate30-bitrate2500/output-VP9-L1T3-L0T2.ivf'
        ))
    inputs.append(
        base_path.joinpath(
            'tests-buf_initial_sz-500/gipsrestat-1280x720_20210211.vp9-remux.ivf/1280x720-framerate30-bitrate2500/output-VP9-L1T1-L0T0.ivf'
        ))
    inputs.append(
        base_path.joinpath(
            'tests-buf_initial_sz-1000/gipsrestat-1280x720_20210211.vp9-remux.ivf/1280x720-framerate30-bitrate2500/output-VP9-L1T1-L0T0.ivf'
        ))

    output_dir = pathlib.Path().joinpath('ffmpeg_ssim').resolve()
    shutil.rmtree(output_dir, ignore_errors=True)
    output_dir.mkdir(exist_ok=True)

    for input in inputs:
        m = re.match(
            r'.*tests-buf_initial_sz-(?P<bufsize>[0-9]+).*bitrate(?P<bitrate>[0-9]+).*VP9-(?P<smode>.*)-',
            str(input))
        if not m:
            raise RuntimeError(f'Invalid: {suite}')
        '''
        print(m['bufsize'])
        print(m['bitrate'])
        print(m['smode'])
        '''
        output = f"buf_initial_sz{m['bufsize']}-bitrate{m['bitrate']}-{m['smode']}.log"
        output = output_dir.joinpath(output)
        print(output)

        cmd = f'ffmpeg -i {input} -i {ref} -lavfi  ssim;[0:v][1:v]psnr  -f null -'
        run_shell(cmd, log_file=output)

    return 0


if __name__ == '__main__':
    sys.exit(main())
