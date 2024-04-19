#!/usr/bin/python3 -u

import sys
import os
import re
import pathlib
import subprocess
import argparse
import shutil

# local modules
from pm_shell import run_shell as run_shell


def install_deps(packages=None):
    os_release = None
    with open('/etc/os-release', encoding="utf-8") as f:
        os_release = f.readline()

    if os_release and re.search('Ubuntu', os_release):
        print(f'OS Ubuntu')

        if packages:
            cmd = f'sudo -E apt install -y ' + packages
            run_shell(cmd)
    else:
        raise RuntimeError(f'Unsupported OS {os_release}')


def clone_git_repo(url, git_revision, dst, clean=None):
    cwd = os.getcwd()

    if dst.is_dir() and clean:
        cmd = f'rm -rf {dst}'
        run_shell(cmd)

    if not dst.is_dir():
        cmd = f'git clone {url} {dst}'
        run_shell(cmd)

        os.chdir(str(dst))

        cmd = f'git checkout {git_revision}'
        run_shell(cmd)

    os.chdir(cwd)
    return


def autogen_build(dst, configure=''):
    if not dst.exists():
        raise RuntimeError(f'{dst} not existed')

    cwd = os.getcwd()
    os.chdir(str(dst))

    cmd = f'./autogen.sh {configure}'
    run_shell(cmd)

    cmd = f'make -j 8'
    run_shell(cmd)

    cmd = f'make install'
    run_shell(cmd)

    os.chdir(cwd)
    return


def configure_build(dst, configure=''):
    if not dst.exists():
        raise RuntimeError(f'{dst} not existed')

    cwd = os.getcwd()
    os.chdir(str(dst))

    cmd = f'./configure {configure}'
    run_shell(cmd)

    cmd = f'make -j 8'
    run_shell(cmd)

    cmd = f'make install'
    run_shell(cmd)

    os.chdir(cwd)
    return

#-DCMAKE_INSTALL_PREFIX={prefix}
def cmake_build(dst, configure='', install_opts=''):
    if not dst.exists():
        raise RuntimeError(f'{dst} not existed')

    cwd = os.getcwd()

    cmake_dir = dst.joinpath('cmake_build').resolve()
    if (cmake_dir.exists()):
        shutil.rmtree(str(cmake_dir))

    cmake_dir.mkdir(exist_ok=True)
    os.chdir(str(cmake_dir))

    cmd = f'cmake {configure} ..'
    run_shell(cmd)

    cmd = f'make -j 8'
    run_shell(cmd)

    cmd = f'make {install_opts} install'
    run_shell(cmd)

    os.chdir(cwd)
    return

def meson_build(dst, configure='', install_opts=''):
    if not dst.exists():
        raise RuntimeError(f'{dst} not existed')

    cwd = os.getcwd()

    meson_dir = dst.joinpath('meson_build').resolve()
    if (meson_dir.exists()):
        shutil.rmtree(str(meson_dir))

    meson_dir.mkdir(exist_ok=True)
    os.chdir(str(meson_dir))

    cmd = f'meson .. {configure}'
    run_shell(cmd)

    cmd = f'ninja install'
    run_shell(cmd)

    os.chdir(cwd)
    return

