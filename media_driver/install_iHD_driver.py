#!/usr/bin/python3 -u

import sys
import os
import re
import pathlib
import subprocess
import argparse
import shutil

global_pwd = pathlib.Path().resolve()

global_build = global_pwd.joinpath('third_party')
global_prefix = global_pwd.joinpath('out')


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
    print(result)
    return result


def install_deps():
    os_release = None
    with open('/etc/os-release', encoding="utf-8") as f:
        os_release = f.readline()

    if os_release and re.search('Ubuntu', os_release):
        print(f'OS Ubuntu')
    else:
        raise RuntimeError(f'Unsupported OS {os_release}')


def clone_git_repo(url, git_revision, dst, clean=None):
    cwd = os.getcwd()

    if dst.is_dir() and clean:
        cmd = f'rm -rf {str(dst)}'
        exec_bash(cmd)

    if not dst.is_dir():
        cmd = f'git clone {url} {str(dst)}'
        exec_bash(cmd)

        os.chdir(str(dst))

        cmd = f'git checkout {git_revision}'
        exec_bash(cmd)

    os.chdir(cwd)
    return

def autogen_build(dst, configure):
    cwd = os.getcwd()
    os.chdir(str(dst))

    cmd = f'./autogen.sh --prefix={global_prefix} {configure}'
    exec_bash(cmd)

    cmd = f'make -j'
    exec_bash(cmd)

    cmd = f'make install'
    exec_bash(cmd)

    os.chdir(cwd)
    return

def configure_build(dst, configure):
    cwd = os.getcwd()
    os.chdir(str(dst))

    cmd = f'./configure --prefix={str(global_prefix)} {configure}'
    exec_bash(cmd)

    cmd = f'make -j'
    exec_bash(cmd)

    cmd = f'make install'
    exec_bash(cmd)

    os.chdir(cwd)
    return


def cmake_build(dst, configure, install_opts=''):
    cwd = os.getcwd()

    cmake_dir = dst.joinpath('cmake_build').resolve()

    if (cmake_dir.exists()):
        shutil.rmtree(str(cmake_dir))

    cmake_dir.mkdir(exist_ok=True)
    os.chdir(str(cmake_dir))

    cmd = f'cmake -DCMAKE_INSTALL_PREFIX={str(PREFIX)} {configure} ..'
    exec_bash(cmd)

    cmd = f'make -j'
    exec_bash(cmd)

    cmd = f'make {install_opts} install'
    exec_bash(cmd)

    os.chdir(cwd)
    return


def install_libva(version=None):
    name = 'libva'
    url = f'git@github.com:intel/{name}.git'

    dst = global_build.joinpath(name)
    clone_git_repo(url, version, dst, None)

    configure = ''
    autogen_build(dst, configure)

    return


def install_libva_utils(version=None):
    name = 'libva-utils'
    url = f'git@github.com:intel/{name}.git'

    dst = global_build.joinpath(name)
    clone_git_repo(url, version, dst, None)

    # --disable-x11
    configure = '--disable-wayland'
    autogen_build(dst, configure)

    return


def install_gmmlib(version=None):
    name = 'gmmlib'
    url = f'git@github.com:intel/{name}.git'

    dst = global_build.joinpath(name)
    clone_git_repo(url, version, dst, None)

    return


def install_iHD_driver(version=None, non_free=True):
    name = 'media-driver'
    url = f'git@github.com:intel/{name}.git'

    dst = global_build.joinpath(name)
    clone_git_repo(url, version, dst, None)

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
    install_deps()

    # build
    my_env = os.environ
    if not 'PKG_CONFIG_PATH' in my_env:
        my_env['PKG_CONFIG_PATH'] = ''
    my_env[
        'PKG_CONFIG_PATH'] = f"{str(global_prefix)}/lib/pkgconfig:{my_env['PKG_CONFIG_PATH']}"

    install_libva('2.18.0')
    install_libva_utils('2.18.0')
    install_gmmlib('intel-gmmlib-22.3.5')
    install_iHD_driver('master')
    #install_iHD_driver('intel-media-23.1.6')


if __name__ == '__main__':
    sys.exit(main())
