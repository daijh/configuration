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

global_pwd = pathlib.Path().resolve()

global_build = global_pwd.joinpath('third_party')
global_prefix = global_pwd.joinpath('out')


def install_libva(version=None):
    name = 'libva'
    url = f'git@github.com:intel/{name}.git'

    dst = global_build.joinpath(name)
    pm_packages.clone_git_repo(url, version, dst, None)

    configure = f'--prefix={global_prefix}'
    pm_packages.autogen_build(dst, configure)

    return


def install_libva_utils(version=None):
    name = 'libva-utils'
    url = f'git@github.com:intel/{name}.git'

    dst = global_build.joinpath(name)
    pm_packages.clone_git_repo(url, version, dst, None)

    # --disable-x11
    configure = '--prefix={global_prefix} --disable-wayland'
    pm_packages.autogen_build(dst, configure)

    return


def install_gmmlib(version=None):
    name = 'gmmlib'
    url = f'git@github.com:intel/{name}.git'

    dst = global_build.joinpath(name)
    pm_packages.clone_git_repo(url, version, dst, None)

    configure = f'-DCMAKE_INSTALL_PREFIX={global_prefix} -DBUILD_TYPE=debug'
    pm_packages.cmake_build(dst, configure)

    return


def install_iHD_driver(version=None, non_free=True):
    name = 'media-driver'
    url = f'git@github.com:intel/{name}.git'

    dst = global_build.joinpath(name)
    pm_packages.clone_git_repo(url, version, dst, None)

    configure = f'-DCMAKE_INSTALL_PREFIX={global_prefix} -DBUILD_TYPE=debug'
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
    args = parser.parse_args()

    # install deps
    pm_packages.install_deps()

    # Set pkg_config_path to env
    pkg_config_path = global_prefix.joinpath('lib/pkgconfig')
    pm_shell.set_env('PKG_CONFIG_PATH', pkg_config_path)

    # build
    install_libva('2.18.0')
    #install_libva_utils('2.18.0')
    install_gmmlib('intel-gmmlib-22.3.5')
    install_iHD_driver('master')
    #install_iHD_driver('intel-media-23.1.6')


if __name__ == '__main__':
    sys.exit(main())
