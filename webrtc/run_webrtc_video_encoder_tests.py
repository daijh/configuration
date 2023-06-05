#!/usr/bin/python3 -E

import sys
import os
import re
import pathlib
import subprocess
import argparse
import shutil

# pwd
PWD = pathlib.Path().resolve()

# executatble prefix
ROOT = PWD


def exec_bash(cmd, check=True, env=None, log_file=None):
    print(f'{cmd}\n')

    if log_file:
        print(f'Write log: {log_file}\n')

        result = subprocess.run(cmd.split(),
                                check=check,
                                env=env,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                text=True)
        with open(log_file, 'w', encoding="utf-8") as f:
            f.write(result.stdout)
    else:
        result = subprocess.run(cmd.split(), check=check, env=env)

    result.stdout = None

    print(result)
    return result


def make_default_pattern_test_suit():
    pattern_test_suit = []

    codecs = ['vp8', 'vp9', 'h264', 'av1']
    scalability_modes = ['L1T1', 'L1T3', 'L3T3_KEY']

    encode_settings = []
    encode_settings.append({
        'width': 1280,
        'height': 640,
        'frame_rate': 30,
        'bitrate_kbps': 1500
    })
    encode_settings.append({
        'width': 640,
        'height': 320,
        'frame_rate': 30,
        'bitrate_kbps': 500
    })
    encode_settings.append({
        'width': 320,
        'height': 180,
        'frame_rate': 30,
        'bitrate_kbps': 150
    })

    # case
    pattern_test = {}
    pattern_test['pattern'] = 0
    pattern_test['codecs'] = codecs
    pattern_test['scalability_modes'] = scalability_modes
    pattern_test['encode_settings'] = encode_settings

    pattern_test_suit.append(pattern_test)

    # case
    pattern_test = {}
    pattern_test['pattern'] = 1
    pattern_test['codecs'] = codecs
    pattern_test['scalability_modes'] = scalability_modes
    pattern_test['encode_settings'] = encode_settings

    pattern_test_suit.append(pattern_test)

    # return all test cases
    return pattern_test_suit


def run_pattern_tests(pattern_test_suit, force=None):
    output_dir = PWD.joinpath(f'video_encoder_tests-pattern')
    if (output_dir.exists()):
        if (force):
            shutil.rmtree(str(output_dir))
        else:
            print(f'Error, output dir allready exists, {output_dir}')
            sys.exit(1)

    for pattern_test in pattern_test_suit:
        pattern = pattern_test['pattern']
        codecs = pattern_test['codecs']
        scalability_modes = pattern_test['scalability_modes']

        # pattern dir
        pattern_dir_path = output_dir.joinpath(f'pattern{pattern}')
        pattern_dir_path.mkdir(parents=True, exist_ok=False)

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

                    cmd = f'video_encoder --video_codec={codec} --scalability_mode={scalability_mode} ' \
                            f'--width={encode_setting["width"]} --height={encode_setting["height"]} ' \
                            f'--frame_rate={encode_setting["frame_rate"]} --bitrate_kbps={encode_setting["bitrate_kbps"]} ' \
                            f'--raw_frame_generator={pattern} '
                    exec_bash(cmd,
                              check=False,
                              log_file=str(log_file.resolve()))

    return


def make_ivf_test_suit():
    ivf_input_test_suit = []

    codecs = ['vp8', 'vp9', 'h264', 'av1']
    scalability_modes = ['L1T1', 'L1T3', 'L3T3_KEY']

    # case
    ivf_input_test = {}
    ivf_input_test[
        'ivf_input'] = '/home/webrtc/third_party/test_streams/vp9_lossless_static/youtube_screenshot_static.ivf'
    ivf_input_test['codecs'] = codecs
    ivf_input_test['scalability_modes'] = scalability_modes

    encode_settings = []
    encode_settings.append({
        'width': 1536,
        'height': 748,
        'frame_rate': 30,
        'bitrate_kbps': 2250
    })
    ivf_input_test['encode_settings'] = encode_settings

    ivf_input_test_suit.append(ivf_input_test)

    # case
    ivf_input_test = {}
    ivf_input_test[
        'ivf_input'] = '/home/webrtc/third_party/test_streams/vp9_lossless_static/gipsrestat-320x180_static.vp9.ivf'
    ivf_input_test['codecs'] = codecs
    ivf_input_test['scalability_modes'] = scalability_modes

    encode_settings = []
    encode_settings.append({
        'width': 320,
        'height': 180,
        'frame_rate': 30,
        'bitrate_kbps': 288
    })
    ivf_input_test['encode_settings'] = encode_settings

    ivf_input_test_suit.append(ivf_input_test)

    # return all test cases
    return ivf_input_test_suit


def run_ivf_input_tests(ivf_test_suit, force=None):
    output_dir = PWD.joinpath(f'video_encoder_tests-ivf')
    if (output_dir.exists()):
        if (force):
            shutil.rmtree(str(output_dir))
        else:
            print(f'Error, output dir allready exists, {output_dir}')
            sys.exit(1)

    for ivf_test in ivf_test_suit:
        ivf_input = ivf_test['ivf_input']
        codecs = ivf_test['codecs']
        scalability_modes = ivf_test['scalability_modes']

        # check input exists
        ivf_path = pathlib.Path(ivf_input).resolve()
        if (not ivf_path.exists()):
            print(f'ivf input dose not exist, {ivf_input}')
            sys.exit(1)

        # pattern dir
        pattern_dir_path = output_dir.joinpath(f'{ivf_path.name}')
        pattern_dir_path.mkdir(parents=True, exist_ok=False)

        for encode_setting in ivf_test['encode_settings']:
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

                    cmd = f'video_encoder --video_codec={codec} --scalability_mode={scalability_mode} ' \
                            f'--width={encode_setting["width"]} --height={encode_setting["height"]} ' \
                            f'--frame_rate={encode_setting["frame_rate"]} --bitrate_kbps={encode_setting["bitrate_kbps"]} ' \
                            f'--ivf_input_file={str(ivf_path)} '
                    exec_bash(cmd,
                              check=False,
                              log_file=str(log_file.resolve()))

    return


if __name__ == '__main__':
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
    parser.add_argument('--ivf-tests',
                        dest='run_ivf_tests',
                        action='store_true',
                        default=False,
                        help="Run ivf input tests")
    args = parser.parse_args()

    if args.root:
        ROOT = pathlib.Path(args.root).resolve()
        print(f'Set ROOT, {ROOT}')

    # Set env
    # WebRTC
    PREFIX = ROOT.joinpath('src/out/Default')

    my_env = os.environ
    if not 'PATH' in my_env:
        my_env['PATH'] = ''
    my_env['PATH'] = f"{str(PREFIX)}:{my_env['PATH']}"

    if args.run_ivf_tests:
        ivf_test_suit = make_ivf_test_suit()
        run_ivf_input_tests(ivf_test_suit, force=args.force_delete_outputs)
    else:
        pattern_test_suit = make_default_pattern_test_suit()
        run_pattern_tests(pattern_test_suit, force=args.force_delete_outputs)
