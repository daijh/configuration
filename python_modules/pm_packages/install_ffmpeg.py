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
        packages += f'build-essential cmake libtool wget tcl '
        packages += f'yasm libssl-dev '
        packages += f'libsdl2-dev libjpeg-dev '
        packages += f'libfdk-aac-dev libmp3lame-dev '
        packages += f'libx264-dev libx265-dev '

        cmd = f'sudo -E apt install -y ' + packages
        run_shell(cmd)
    else:
        raise RuntimeError(f'Unsupported OS {os_release}')


def build_ffmpeg(dst, prefix):
    configure = f'--prefix={prefix} --enable-shared --enable-static '\
                '--disable-vaapi --enable-gpl --enable-nonfree ' \
               ' --enable-libmp3lame --enable-libfdk-aac ' \
                '--enable-libvpx --enable-libx264 --enable-libx265 --enable-libaom'
    pm_packages.configure_build(dst, configure)

    return


def install_ffmpeg_gitrepo(source_dir, prefix):
    name = 'ffmpeg'
    url = f'https://git.ffmpeg.org/{name}'
    version = ''

    dst = source_dir.joinpath(name)
    pm_packages.clone_git_repo(url, version, dst, None)
    build_ffmpeg(dst, prefix)
    return


def install_ffmpeg(source_dir, prefix):
    version = 'n6.0'
    name = f'FFmpeg-{version}'
    download = f'{version}.tar.gz'
    url = f'https://github.com/FFmpeg/FFmpeg/archive/{download}'

    dst = source_dir.joinpath(name)

    # wget
    cwd = os.getcwd()
    os.chdir(str(source_dir))

    if not source_dir.joinpath(download).exists():
        cmd = f'wget {url}'
        run_shell(cmd)

    if not dst.exists():
        cmd = f'tar -zvxf {download}'
        run_shell(cmd)

    # build
    build_ffmpeg(dst, prefix)
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

    if not source_dir.exists():
        source_dir.mkdir(parents=True, exist_ok=True)

    # Set pkg_config_path to env
    pkg_config_path = prefix.joinpath('lib/pkgconfig')
    pm_shell.set_env('PKG_CONFIG_PATH', pkg_config_path)

    # install deps
    if args.install_deps:
        install_deps()

    # build
    if args.use_git:
        install_ffmpeg_gitrepo(source_dir, prefix)
    else:
        install_ffmpeg(source_dir, prefix)


if __name__ == '__main__':
    sys.exit(main())
