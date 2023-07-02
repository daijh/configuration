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
    configure = f'--prefix={prefix} --disable-wayland'
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
    out = pwd.joinpath('out').resolve()

    # version
    libva_version = '2.18.0'
    gmmlib_version = 'intel-gmmlib-22.3.5'
    iHD_version = 'master'
    prefix = out.joinpath(f'iHD-{iHD_version}-libva-{libva_version}').resolve()

    # Set pkg_config_path to env
    pkg_config_path = prefix.joinpath('lib/pkgconfig').resolve()
    pm_shell.set_env('PKG_CONFIG_PATH', pkg_config_path)

    # install deps
    if args.install_deps:
        install_deps()

    # build
    install_libva(source_dir, prefix, libva_version)
    install_libva_utils(source_dir, prefix, libva_version)
    install_gmmlib(source_dir, prefix, gmmlib_version)
    install_iHD_driver(source_dir, prefix, iHD_version)


if __name__ == '__main__':
    sys.exit(main())
