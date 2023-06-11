#!/usr/bin/python3 -u

import sys
import os
import re
import pathlib
import subprocess
import argparse
import shutil


def run_shell(cmd, check=True, env=None, log_file=None, shell=False):
    print(f'{cmd}\n')

    if log_file:
        print(f'Write log: {log_file}\n')

        result = subprocess.run(cmd.split(),
                                check=check,
                                env=env,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                shell=shell,
                                text=True)
        with open(log_file, 'w', encoding="utf-8") as f:
            f.write(result.stdout)
    else:
        result = subprocess.run(cmd.split(), check=check, env=env)

    result.stdout = None
    print(f'{result}\n')
    return result


def main() -> int:
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument('-p',
                        '--password',
                        dest='password',
                        action='store',
                        default=None,
                        help="Specify password")
    args = parser.parse_args()

    if not args.password:
        raise RuntimeError(f'{password} it not set')

    cmd = f'killall gnome-keyring-daemon'
    run_shell(cmd, check=True, shell=True)

    cmd = f"echo -n '{args.password}' | gnome-keyring-daemon -l -d"
    run_shell(cmd, check=True, shell=True)

    cmd = f'gnome-keyring-daemon -s'
    run_shell(cmd, check=True, shell=True)

    '''
    cmd = f'systemctl --user daemon-reload'
    run_shell(cmd, check=True, shell=True)
    '''

    cmd = f'systemctl --user restart gnome-remote-desktop'
    run_shell(cmd, check=True, shell=True)

    cmd = f'systemctl --user status gnome-remote-desktop'
    run_shell(cmd, check=True, shell=True)

    print('Done')
    return 0


if __name__ == '__main__':
    sys.exit(main())
