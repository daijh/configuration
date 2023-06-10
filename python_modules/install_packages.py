#!/usr/bin/python3 -E

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
        packages = ''
        packages += f'build-essential cmake libtool wget tcl '
        packages += f'yasm libssl-dev '
        packages += f'libsdl2-dev libjpeg-dev '
        packages += f'libfdk-aac-dev libmp3lame-dev '
        packages += f'libx264-dev libx265-dev '

        cmd = f'sudo -E apt install -y ' + packages
        exec_bash(cmd)
    else:
        print(f'Unsupported OS {os_release}')
        sys.exit(1)


def install_dlog(source_dir, prefix):
    name = 'dlog'
    url = f'git@github.com:daijh/{name}.git'
    version = ''
    configure = f'-DCMAKE_INSTALL_PREFIX={prefix} -DCMAKE_INSTALL_LIBDIR=lib'

    dst = source_dir.joinpath(name)
    pm_packages.clone_git_repo(url, version, dst, None)
    pm_packages.cmake_build(dst, configure, install_opts=f'DESTDIR={prefix}')

    return


def install_svt_hevc(source_dir, prefix):
    name = 'SVT-HEVC'
    url = f'https://github.com/OpenVisualCloud/{name}'
    version = ''
    configure = f'-DCMAKE_INSTALL_PREFIX={prefix} -DCMAKE_INSTALL_LIBDIR=lib'

    dst = source_dir.joinpath(name)
    pm_packages.clone_git_repo(url, version, dst, None)
    pm_packages.cmake_build(dst, configure)

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

    # build
    install_svt_hevc(source_dir, prefix)
    '''
    install_libvpx()
    install_libaom()

    install_ffmpeg()
    '''

    install_dlog(source_dir, prefix)

    print('Done')
    return 0


if __name__ == '__main__':
    sys.exit(main())
