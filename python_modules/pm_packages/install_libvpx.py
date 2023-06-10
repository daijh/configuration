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
import pm_packages
from pm_shell import exec_bash as exec_bash


def install_deps():
    os_release = None
    with open('/etc/os-release', encoding="utf-8") as f:
        os_release = f.readline()

    if os_release and re.search('Ubuntu', os_release):
        print(f'OS Ubuntu')
        '''
        packages = ''
        packages += f'build-essential cmake libtool wget tcl '

        cmd = f'sudo -E apt install -y ' + packages
        exec_bash(cmd)
        '''
    else:
        raise RuntimeError(f'Unsupported OS {os_release}')


def build_libvpx(dst, prefix):
    configure = f'--prefix={prefix} --enable-vp8 --enable-vp9 --enable-vp9-highbitdepth --enable-pic --enable-shared --disable-static'
    pm_packages.configure_build(dst, configure)

    return


def install_libvpx(source_dir, prefix):
    name = 'libvpx'
    url = f'https://chromium.googlesource.com/webm/{name}'
    version = 'v1.13.0'

    dst = source_dir.joinpath(name)
    pm_packages.clone_git_repo(url, version, dst, None)
    build_libvpx(dst, prefix)

    return


def install_libvpx_myrepo(source_dir, prefix):
    name = 'libvpx'

    url = f'git@github.com:daijh/{name}.git'
    version = 'v1.13.0-bitstream-parser'

    dst = source_dir.joinpath(name)
    pm_packages.clone_git_repo(url, version, dst, None)

    build_libvpx(dst, prefix)

    # add origin repo
    cwd = os.getcwd()
    os.chdir(str(dst))

    origin_url = f'https://chromium.googlesource.com/webm/{name}'
    origin_version = ''

    cmd = f'git remote add -f origin_repo ' + origin_url
    exec_bash(cmd, check=False)

    os.chdir(cwd)

    return


def main() -> int:
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument('-r',
                        '--root',
                        dest='root',
                        action='store',
                        default=None,
                        help="Set root install path")
    parser.add_argument('-d',
                        '--deps',
                        dest='install_deps',
                        action='store_true',
                        default=False,
                        help="Install all deps")
    parser.add_argument('-g',
                        '--git',
                        dest='use_git',
                        action='store_true',
                        default=False,
                        help="Use git repo")
    args = parser.parse_args()

    # set pwd
    pwd = pathlib.Path().resolve()
    if args.root:
        pwd = pathlib.Path(args.root).resolve()
    print(f'Set PWD, {pwd}')

    source_dir = pwd.joinpath('third_party')
    prefix = pwd.joinpath('out')

    # install deps
    if args.install_deps:
        install_deps()

    if args.use_git:
        install_libvpx_myrepo(source_dir, prefix)
    else:
        install_libvpx(source_dir, prefix)


if __name__ == '__main__':
    sys.exit(main())
