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


def install_deps():
    os_release = None
    with open('/etc/os-release', encoding="utf-8") as f:
        os_release = f.readline()

    if os_release and re.search('Ubuntu', os_release):
        print(f'OS Ubuntu')
        packages = ''
        packages += f'vulkan-tools libvulkan-dev vulkan-validationlayers-dev spirv-tools '
        packages += f'libglm-dev '

        cmd = f'sudo -E apt install -y ' + packages
        run_shell(cmd)
    else:
        raise RuntimeError(f'Unsupported OS {os_release}')


def install_shaderc(source_dir, prefix):
    name = 'shaderc'
    url = f'git@github.com:google/{name}.git'
    version = 'v2024.1'

    dst = source_dir.joinpath(name)
    pm_packages.clone_git_repo(url, version, dst, clean=None)

    os.chdir(str(dst))
    cmd = f'./utils/git-sync-deps'
    run_shell(cmd)

    configure = f'-Bbuild -GNinja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_INSTALL_PREFIX={prefix}'
    cmd = f'cmake {configure}'
    run_shell(cmd)

    cmd = f'autoninja -C build'
    run_shell(cmd)

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

    install_shaderc(source_dir, prefix)

if __name__ == '__main__':
    sys.exit(main())