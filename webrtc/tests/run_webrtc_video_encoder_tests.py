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


def make_test_suite(include_pattern_tests=True, include_ivf_tests=True):
    test_suite = []

    #codecs = ['vp8', 'vp9', 'h264', 'av1']
    #codecs = ['vp8', 'vp9']
    codecs = ['vp9']
    #scalability_modes = ['L1T1', 'L1T3', 'L3T3_KEY']
    scalability_modes = ['L1T1', 'L1T3']
    #scalability_modes = ['L3T3_KEY', 'L3T3']

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

    # pattern case
    if include_pattern_tests:
        for pattern in range(2):
            test = {}
            test['pattern'] = pattern
            test['codecs'] = codecs
            test['scalability_modes'] = scalability_modes
            test['encode_settings'] = encode_settings

            test_suite.append(test)

    if include_ivf_tests:
        # ivf case
        ivf_dir = pathlib.Path(
            '/home/webrtc/third_party/test_streams/vp9_lossless_static'
        ).resolve()

        ivf_files = []
        ivf_files.append(ivf_dir.joinpath('youtube_screenshot_static.ivf'))
        ivf_files.append(ivf_dir.joinpath('gipsrestat-320x180_static.vp9.ivf'))

        for ivf in ivf_files:
            test = {}
            test['ivf'] = ivf
            test['codecs'] = codecs
            test['scalability_modes'] = scalability_modes
            test['encode_settings'] = encode_settings

            test_suite.append(test)

    # return all test cases
    for p in test_suite:
        print(p)

    return test_suite


def run_tests(test_suite, force, output_dir):
    key_frame_interval = 100
    frames = 300

    if output_dir.exists():
        if force:
            shutil.rmtree(str(output_dir))
        else:
            raise RuntimeError(
                f'Error, output dir allready exists, {output_dir}')

    for test_case in test_suite:
        codecs = test_case['codecs']
        scalability_modes = test_case['scalability_modes']

        # pattern dir
        if 'pattern' in test_case:
            pattern_dir_path = output_dir.joinpath(
                f"pattern{test_case['pattern']}")
            pattern_dir_path.mkdir(parents=True, exist_ok=False)
        elif 'ivf' in test_case:
            pattern_dir_path = output_dir.joinpath(f"{test_case['ivf'].name}")
            pattern_dir_path.mkdir(parents=True, exist_ok=False)
        else:
            raise RuntimeError(f'Invalid {test_case}')

        for encode_setting in test_case['encode_settings']:
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

                    if 'pattern' in test_case:
                        cmd += f"--raw_frame_generator={test_case['pattern']} "
                    elif 'ivf' in test_case:
                        cmd += f"--ivf_input_file={test_case['ivf'] }"
                    else:
                        raise RuntimeError(f'Invalid {test_case}')

                    run_shell(cmd,
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
    parser.add_argument('-o',
                        '--output',
                        dest='output',
                        action='store',
                        default='webrtc_video_encoder_tests',
                        help="Specify output")
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

    # output
    pwd = pathlib.Path().resolve()
    if not args.output:
        output_dir = pwd.joinpath(f'webrtc_video_encoder_tests')
    else:
        output_dir = pwd.joinpath(f'tests-{args.output}')

    if len(test_suite):
        run_tests(test_suite,
                  force=args.force_delete_outputs,
                  output_dir=output_dir)

    return 0


if __name__ == '__main__':
    sys.exit(main())
