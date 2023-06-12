#!/usr/bin/python3 -u

import sys
import os
import re
import pathlib
import subprocess
import argparse
import shutil
import csv
from operator import itemgetter, attrgetter

# local modules
import pm_shell
import pm_video
from pm_shell import run_shell as run_shell

# pwd
global_pwd = pathlib.Path().resolve()


def parse_results(input_dir) -> int:
    if not input_dir.exists():
        raise RuntimeError(f'input dir does not exist, {input_dir}')

    output = f'output.csv'

    results = []

    files = input_dir.glob('**/*.ivf')
    for file in files:
        result = {}

        trace_header_file = file.parent.joinpath(f'{file.name}.trace_header')
        pm_video.trace_header(file, trace_header_file)

        # vp9-L1T1
        codec_scalability_mode = file.parent.parent.parent.name
        m = re.match(r"(?P<codec>.*)-(?P<scalability_mode>.*)",
                     codec_scalability_mode)
        if not m:
            raise RuntimeError(f'invalid {codec_scalability_mode}')

        result['input'] = file.parent.parent.parent.parent.parent.name
        result['codec'] = m.group('codec')
        result['encode_settings'] = file.parent.parent.parent.parent.name
        result['scalability_mode'] = m.group('scalability_mode')
        result['ivf_file'] = file.name
        result['size'] = file.stat().st_size

        # bitrate
        m = re.match(r".*framerate(?P<frame_rate>[0-9]+).*",
                     result['encode_settings'])
        if not m:
            raise RuntimeError(f"invalid {result['encode_settings']}")
        frame_rate = int(m.group('frame_rate'))

        result['frames'] = int(pm_video.video_frames(trace_header_file))
        result['bitrate_kbps'] = int(8 * frame_rate * result['size'] /
                                     result['frames'] / 1000)

        result[
            'test_suite'] = file.parent.parent.parent.parent.parent.parent.name

        print(result)
        results.append(result)

    sorted_results = sorted(results,
                            key=itemgetter('input', 'encode_settings', 'codec',
                                           'scalability_mode', 'ivf_file'),
                            reverse=False)

    if len(sorted_results) == 0:
        raise RuntimeError(f'empty results')

    with open(f'{output}', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, dialect='excel')

        # parse test_suite and value
        values_dict = {}
        test_suites = set()
        test_suites_item_names = ['size', 'frames', 'bitrate_kbps']
        for r in sorted_results:
            # retrieve test_suite
            test_suites.add(r['test_suite'])

            # retrieve value
            key = f"{r['input']} {r['codec']} {r['encode_settings']} {r['scalability_mode']} {r['ivf_file']}"
            if not key in values_dict:
                values_dict[key] = {}
            values_dict[key][r['test_suite']] = {
                'size': r['size'],
                'frames': r['frames'],
                'bitrate_kbps': r['bitrate_kbps']
            }

        test_suites = sorted(test_suites)

        # header
        fieldnames = [
            'Input', 'Video Codec', 'Encode Settings', 'Scalability Mode',
            'Name'
        ]
        for test_suit in test_suites:
            for name in test_suites_item_names[:1]:
                fieldnames.append(f'{test_suit}-{name}')
            for name in test_suites_item_names[1:]:
                fieldnames.append(f'{name}')

        writer.writerow(fieldnames)

        print(f'header: {fieldnames}')

        # write csv
        last_key = []
        rows = []
        for r in sorted_results:
            key = f"{r['input']} {r['codec']} {r['encode_settings']} {r['scalability_mode']} {r['ivf_file']}"

            # skip repeated key
            if last_key == key:
                continue
            last_key = key

            row = key.split()
            # retrieve value
            for test_suite in test_suites:
                row += values_dict[key][test_suite].values()
            rows.append(row)

        # delete duplicate
        csv_key = None
        csv_key_size = len(rows[0]) - len(test_suites)
        for row in rows:
            if not csv_key:
                csv_key = row[:csv_key_size]
                continue

            # update csv_key
            i = 0
            for i in range(csv_key_size):
                if row[i] != csv_key[i]:
                    break
                row[i] = ""

            csv_key[i:] = row[i:csv_key_size]

        # write
        writer.writerows(rows)

    print(f'Writed: {output}')
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument('input', default=None, help="Specify input")
    parser.add_argument('-f',
                        '--force',
                        dest='force_delete_outputs',
                        action='store_true',
                        help="Force delete outputs")
    args = parser.parse_args()

    input_dir = pathlib.Path(args.input).resolve()
    if not input_dir.exists():
        raise RuntimeError(f'Dir does not exist: {input_file}')

    parse_results(input_dir)

    return 0


if __name__ == '__main__':
    sys.exit(main())
