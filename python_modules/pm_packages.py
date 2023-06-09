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


def install_deps(packages=None):
    os_release = None
    with open('/etc/os-release', encoding="utf-8") as f:
        os_release = f.readline()

    if os_release and re.search('Ubuntu', os_release):
        print(f'OS Ubuntu')

        if packages:
            cmd = f'sudo -E apt install -y ' + packages
            exec_bash(cmd)
    else:
        raise RuntimeError(f'Unsupported OS {os_release}')


def clone_git_repo(url, git_revision, dst, clean=None):
    cwd = os.getcwd()

    if dst.is_dir() and clean:
        cmd = f'rm -rf {dst}'
        exec_bash(cmd)

    if not dst.is_dir():
        cmd = f'git clone {url} {dst}'
        exec_bash(cmd)

        os.chdir(str(dst))

        cmd = f'git checkout {git_revision}'
        exec_bash(cmd)

    os.chdir(cwd)
    return


def autogen_build(dst, prefix=None, configure=''):
    if not dst.exists():
        raise RuntimeError(f'{dst} not existed')

    if not prefix:
        raise RuntimeError(f'{prefix} is None')

    cwd = os.getcwd()
    os.chdir(str(dst))

    cmd = f'./autogen.sh --prefix={prefix} {configure}'
    exec_bash(cmd)

    cmd = f'make -j'
    exec_bash(cmd)

    cmd = f'make install'
    exec_bash(cmd)

    os.chdir(cwd)
    return


def configure_build(dst, prefix=None, configure=''):
    if not dst.exists():
        raise RuntimeError(f'{dst} not existed')

    if not prefix:
        raise RuntimeError(f'{prefix} is None!')

    cwd = os.getcwd()
    os.chdir(str(dst))

    cmd = f'./configure --prefix={prefix} {configure}'
    exec_bash(cmd)

    cmd = f'make -j'
    exec_bash(cmd)

    cmd = f'make install'
    exec_bash(cmd)

    os.chdir(cwd)
    return


def cmake_build(dst, prefix=None, configure='', install_opts=''):
    if not dst.exists():
        raise RuntimeError(f'{dst} not existed')

    if not prefix:
        raise RuntimeError(f'{prefix} is None!')

    cwd = os.getcwd()

    cmake_dir = dst.joinpath('cmake_build').resolve()

    if (cmake_dir.exists()):
        shutil.rmtree(str(cmake_dir))

    cmake_dir.mkdir(exist_ok=True)
    os.chdir(str(cmake_dir))

    cmd = f'cmake -DCMAKE_INSTALL_PREFIX={prefix} {configure} ..'
    exec_bash(cmd)

    cmd = f'make -j'
    exec_bash(cmd)

    cmd = f'make {install_opts} install'
    exec_bash(cmd)

    os.chdir(cwd)
    return
