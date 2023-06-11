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
from pm_shell import run_shell as run_shell


def install_libva(source_dir, prefix, version):
    name = 'libva'
    url = f'git@github.com:intel/{name}.git'

    dst = source_dir.joinpath(name)
    pm_packages.clone_git_repo(url, version, dst, None)

    configure = f'--prefix={prefix}'
    pm_packages.autogen_build(dst, configure)

    return


def install_libva_utils(source_dir, prefix, version):
    name = 'libva-utils'
    url = f'git@github.com:intel/{name}.git'

    dst = source_dir.joinpath(name)
    pm_packages.clone_git_repo(url, version, dst, None)

    # --disable-x11
    configure = '--prefix={prefix} --disable-wayland'
    pm_packages.autogen_build(dst, configure)

    return


def install_gmmlib(source_dir, prefix, version):
    name = 'gmmlib'
    url = f'git@github.com:intel/{name}.git'

    dst = source_dir.joinpath(name)
    pm_packages.clone_git_repo(url, version, dst, None)

    configure = f'-DCMAKE_INSTALL_PREFIX={prefix} -DBUILD_TYPE=debug'
    pm_packages.cmake_build(dst, configure)

    return


def install_iHD_driver(source_dir, prefix, version, non_free=True):
    name = 'media-driver'
    url = f'git@github.com:intel/{name}.git'

    dst = source_dir.joinpath(name)
    pm_packages.clone_git_repo(url, version, dst, None)

    configure = f'-DCMAKE_INSTALL_PREFIX={prefix} -DBUILD_TYPE=debug'
    if non_free:
        configure += f' -DENABLE_KERNELS=ON -DENABLE_NONFREE_KERNELS=ON'
    else:
        configure += f' -DENABLE_KERNELS=ON -DENABLE_NONFREE_KERNELS=OFF'
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

    # Set pkg_config_path to env
    pkg_config_path = prefix.joinpath('lib/pkgconfig')
    pm_shell.set_env('PKG_CONFIG_PATH', pkg_config_path)

    # install deps
    if args.install_deps:
        install_deps()

    # build
    install_libva(source_dir, prefix, '2.18.0')
    #install_libva_utils(source_dir, prefix, '2.18.0')
    install_gmmlib(source_dir, prefix, 'intel-gmmlib-22.3.5')
    install_iHD_driver(source_dir, prefix, 'master')
    #install_iHD_driver(source_dir, prefix,'intel-media-23.1.6')


if __name__ == '__main__':
    sys.exit(main())
