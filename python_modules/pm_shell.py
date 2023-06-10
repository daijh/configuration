#!/usr/bin/python3 -u

import sys
import os
import re
import pathlib
import subprocess
import argparse
import shutil


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
    print(f'{result}\n')
    return result


def set_env(env_name, env_value):
    my_env = os.environ
    if not env_name in my_env:
        my_env[env_name] = ''
    my_env[env_name] = f'{(env_value)}:{my_env[env_name]}'

    print(f'Set {env_name}, {env_value}')

