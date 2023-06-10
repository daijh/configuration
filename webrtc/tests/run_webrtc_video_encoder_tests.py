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
from pm_shell import exec_bash as exec_bash

# pwd
global_pwd = pathlib.Path().resolve()


def make_test_suite(include_pattern_tests=True, include_ivf_tests=True):
    pattern_test_suite = []

    #codecs = ['vp8', 'vp9', 'h264', 'av1']
    codecs = ['vp8', 'vp9']
    #scalability_modes = ['L1T1', 'L1T3', 'L3T3_KEY']
    scalability_modes = ['L1T1', 'L1T3']

    encode_settings = []
    # webrtc - max
    encode_settings.append({
        'width': 1280,
        'height': 720,
        'frame_rate': 30,
        'bitrate_kbps': 2500
    })
    encode_settings.append({
        'width': 640,
        'height': 360,
        'frame_rate': 30,
        'bitrate_kbps': 800
    })
    encode_settings.append({
        'width': 320,
        'height': 180,
        'frame_rate': 30,
        'bitrate_kbps': 300
    })
    # webrtc - min
    encode_settings.append({
        'width': 1280,
        'height': 720,
        'frame_rate': 30,
        'bitrate_kbps': 1500
    })
    encode_settings.append({
        'width': 640,
        'height': 360,
        'frame_rate': 30,
        'bitrate_kbps': 500
    })
    encode_settings.append({
        'width': 320,
        'height': 180,
        'frame_rate': 30,
        'bitrate_kbps': 150
    })

    if include_pattern_tests:
        # pattern case
        pattern_test = {}
        pattern_test['pattern'] = 0
        pattern_test['codecs'] = codecs
        pattern_test['scalability_modes'] = scalability_modes
        pattern_test['encode_settings'] = encode_settings

        pattern_test_suite.append(pattern_test)

        # pattern case
        pattern_test = {}
        pattern_test['pattern'] = 1
        pattern_test['codecs'] = codecs
        pattern_test['scalability_modes'] = scalability_modes
        pattern_test['encode_settings'] = encode_settings

        pattern_test_suite.append(pattern_test)

    if include_ivf_tests:
        # ivf case
        ivf_dir = pathlib.Path(
            '/home/webrtc/third_party/test_streams/vp9_lossless_static'
        ).resolve()
        ivf_file = 'youtube_screenshot_static.ivf'

        pattern_test = {}
        pattern_test['ivf'] = ivf_dir.joinpath(ivf_file)
        pattern_test['codecs'] = codecs
        pattern_test['scalability_modes'] = scalability_modes
        pattern_test['encode_settings'] = encode_settings

        pattern_test_suite.append(pattern_test)

        # ivf case
        ivf_dir = pathlib.Path(
            '/home/webrtc/third_party/test_streams/vp9_lossless_static'
        ).resolve()
        ivf_file = 'gipsrestat-320x180_static.vp9.ivf'

        pattern_test = {}
        pattern_test['ivf'] = ivf_dir.joinpath(ivf_file)
        pattern_test['codecs'] = codecs
        pattern_test['scalability_modes'] = scalability_modes
        pattern_test['encode_settings'] = encode_settings

        pattern_test_suite.append(pattern_test)

    # return all test cases
    for p in pattern_test_suite:
        print(p)
    return pattern_test_suite


def run_tests(pattern_test_suite,
              force=None,
              frames=300,
              key_frame_interval=100):
    output_dir = global_pwd.joinpath(f'video_encoder_tests')
    if output_dir.exists():
        if force:
            shutil.rmtree(str(output_dir))
        else:
            raise RuntimeError(
                f'Error, output dir allready exists, {output_dir}')

    for pattern_test in pattern_test_suite:
        codecs = pattern_test['codecs']
        scalability_modes = pattern_test['scalability_modes']

        # pattern dir
        if 'pattern' in pattern_test:
            pattern_dir_path = output_dir.joinpath(
                f"pattern{pattern_test['pattern']}")
            pattern_dir_path.mkdir(parents=True, exist_ok=False)
        elif 'ivf' in pattern_test:
            pattern_dir_path = output_dir.joinpath(
                f"{pattern_test['ivf'].name}")
            pattern_dir_path.mkdir(parents=True, exist_ok=False)
        else:
            raise RuntimeError(f'Invalid {pattern_test}')

        for encode_setting in pattern_test['encode_settings']:
            # test dir
            test_name = f'{encode_setting["width"]}x{encode_setting["height"]}-framerate{encode_setting["frame_rate"]}-bitrate{encode_setting["bitrate_kbps"]}'
            test_dir = pattern_dir_path.joinpath(test_name)
            test_dir.mkdir(parents=True, exist_ok=False)

            os.chdir(str(test_dir))

            for codec in codecs:
                for scalability_mode in scalability_modes:
                    log_dir = test_dir.joinpath(f'logs')
                    log_dir.mkdir(parents=True, exist_ok=True)

                    log_file = log_dir.joinpath(
                        f'{codec}-{scalability_mode}.log')

                    print(f'\n+++Run Case\n')

                    cmd = f'video_encoder --verbose --video_codec={codec} --scalability_mode={scalability_mode} ' \
                            f'--width={encode_setting["width"]} --height={encode_setting["height"]} ' \
                            f'--frame_rate_fps={encode_setting["frame_rate"]} --bitrate_kbps={encode_setting["bitrate_kbps"]} ' \
                            f'--key_frame_interval={key_frame_interval} --frames={frames} '

                    if 'pattern' in pattern_test:
                        cmd += f"--raw_frame_generator={pattern_test['pattern']} "
                    elif 'ivf' in pattern_test:
                        cmd += f"--ivf_input_file={pattern_test['ivf'] }"
                    else:
                        raise RuntimeError(f'Invalid {pattern_test}')

                    exec_bash(cmd,
                              check=False,
                              log_file=str(log_file.resolve()))

    return


def main() -> int:
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument('-r',
                        '--root',
                        dest='root',
                        action='store',
                        default=None,
                        help="Set root install path")
    parser.add_argument('-f',
                        '--force',
                        dest='force_delete_outputs',
                        action='store_true',
                        help="Force delete outputs")
    parser.add_argument('-p',
                        '--pattern-tests',
                        dest='run_pattern_tests',
                        action='store_true',
                        default=False,
                        help="Run pattern input tests")
    parser.add_argument('-ivf',
                        '--ivf-tests',
                        dest='run_ivf_tests',
                        action='store_true',
                        default=False,
                        help="Run ivf input tests")
    parser.add_argument('-a',
                        '--all-tests',
                        dest='run_all_tests',
                        action='store_true',
                        default=False,
                        help="Run all tests")
    args = parser.parse_args()

    root = pathlib.Path().resolve()
    if args.root:
        root = pathlib.Path(args.root).resolve()
    print(f'Set root, {root}')

    # Set webrtc prefix to env
    webrtc_prefix = root.joinpath('src/out/Default')
    pm_shell.set_env('PATH', webrtc_prefix)

    # run
    include_pattern_tests = args.run_pattern_tests or args.run_all_tests
    include_ivf_tests = args.run_ivf_tests or args.run_all_tests
    test_suite = make_test_suite(include_pattern_tests=include_pattern_tests,
                                 include_ivf_tests=include_ivf_tests)

    if len(test_suite):
        run_tests(test_suite,
                  force=args.force_delete_outputs,
                  frames=300,
                  key_frame_interval=100)

    return 0


if __name__ == '__main__':
    sys.exit(main())
