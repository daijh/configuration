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
from pm_shell import exec_bash as exec_bash

# pwd
global_pwd = pathlib.Path().resolve()


def make_vea_test_suite():
    vea_test_suite = []

    codecs = ['vp9']

    scalability_modes = []
    scalability_modes.append({'spatials': 1, 'temporals': 1})
    scalability_modes.append({'spatials': 1, 'temporals': 3})

    # case
    vea_test = {}
    vea_test[
        'input'] = '/home/webrtc/third_party/test_streams/vp9_lossless_static/youtube_screenshot_static.webm'
    vea_test['codecs'] = codecs
    vea_test['scalability_modes'] = scalability_modes

    encode_settings = []
    encode_settings.append({
        'width': 1536,
        'height': 748,
        'frame_rate': 30,
        'bitrate_kbps': 2250
    })
    vea_test['encode_settings'] = encode_settings

    vea_test_suite.append(vea_test)

    # case
    vea_test = {}
    vea_test[
        'input'] = '/home/webrtc/third_party/test_streams/vp9_lossless_static/gipsrestat-320x180_static.vp9.webm'
    vea_test['codecs'] = codecs
    vea_test['scalability_modes'] = scalability_modes

    encode_settings = []
    encode_settings.append({
        'width': 320,
        'height': 180,
        'frame_rate': 30,
        'bitrate_kbps': 288
    })
    vea_test['encode_settings'] = encode_settings

    vea_test_suite.append(vea_test)

    # return all test cases
    return vea_test_suite


def run_vea_tests(vea_test_suite, force=None):
    output_dir = global_pwd.joinpath(f'vea_encoder_tests')
    if output_dir.exists():
        if force:
            shutil.rmtree(str(output_dir))
        else:
            raise RuntimeError(
                f'Error, output dir allready exists, {output_dir}')

    for vea_test in vea_test_suite:
        input_file = vea_test['input']
        codecs = vea_test['codecs']
        scalability_modes = vea_test['scalability_modes']

        # check input exists
        input_path = pathlib.Path(input_file).resolve()
        if not input_path.exists():
            raise RuntimeError(f'ivf input dose not exist, {ivf_input}')

        # pattern dir
        pattern_dir_path = output_dir.joinpath(f'{input_path.name}')
        pattern_dir_path.mkdir(parents=True, exist_ok=False)

        for encode_setting in vea_test['encode_settings']:
            # test dir
            test_name = f'{encode_setting["width"]}x{encode_setting["height"]}-framerate{encode_setting["frame_rate"]}-bitrate{encode_setting["bitrate_kbps"]}'
            test_dir = pattern_dir_path.joinpath(test_name)
            test_dir.mkdir(parents=True, exist_ok=False)

            os.chdir(str(test_dir))

            for codec in codecs:
                for scalability_mode in scalability_modes:
                    codec_mode_name = f'{codec}-L{scalability_mode["spatials"]}T{scalability_mode["temporals"]}'

                    output_path = test_dir.joinpath(f'{codec_mode_name}')
                    log_file = test_dir.joinpath(f'{codec_mode_name}.log')

                    print(f'\n+++Run Case\n')

                    output_path.mkdir(parents=True, exist_ok=False)
                    os.chdir(str(output_path))
                    '''
                            f'--svc_mode=L{scalability_mode["spatials"]}T{scalability_mode["temporals"]} ' \
                            f'--num_spatial_layers={scalability_mode["spatials"]} ' \
                            f'--num_temporal_layers={scalability_mode["temporals"]} ' \
                            f'--gtest_filter=VideoEncoderTest.FlushAtEndOfStream ' \
                            f'--gtest_filter=VideoEncoderTest.BitrateCheck ' \
                    '''

                    cmd = f'video_encode_accelerator_tests ' \
                            f'{str(input_path)} ' \
                            f'--codec={codec} ' \
                            f'--num_spatial_layers={scalability_mode["spatials"]} ' \
                            f'--num_temporal_layers={scalability_mode["temporals"]} ' \
                            f'--bitrate_mode=cbr ' \
                            f'--bitrate={encode_setting["bitrate_kbps"] * 1000} ' \
                            f'--output_bitstream ' \
                            f'--gtest_filter=VideoEncoderTest.FlushAtEndOfStream ' \
                            f'--vmodule=*/media/gpu/*=4 ' \
                            f'--output_folder={str(output_path)} '

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
    parser.add_argument('--svc-tests',
                        dest='run_vp9_svc_tests',
                        action='store_true',
                        default=False,
                        help="Run vp9 svc tests")
    args = parser.parse_args()

    root = pathlib.Path().resolve()
    if args.root:
        root = pathlib.Path(args.root).resolve()
    print(f'Set root, {root}')

    # Set chromium prefix to env
    chromium_prefix = root.joinpath('src/out/Default')
    pm_shell.set_env('PATH', chromium_prefix)

    vea_test_suite = make_vea_test_suite()
    run_vea_tests(vea_test_suite, force=args.force_delete_outputs)


if __name__ == '__main__':
    sys.exit(main())
