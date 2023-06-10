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
        packages = ''
        packages += f'ssh '
        packages += f'apt-file '
        packages += f'vim exuberant-ctags global '
        packages += f'git tig '
        packages += f'tmux tree ack-grep '
        packages += f'build-essential cmake automake libtool '
        packages += f'shfmt cmake-format '
        packages += f'wget curl '
        packages += f'gnome-remote-desktop nfs-common nfs-kernel-server '
        #packages += f'lm-sensors cpuid cpuinfo hwloc '

        cmd = f'sudo -E apt install -y ' + packages
        exec_bash(cmd, check=False)
    else:
        raise RuntimeError(f'Unsupported OS {os_release}')


def install_deps_others():
    os_release = None
    with open('/etc/os-release', encoding="utf-8") as f:
        os_release = f.readline()

    if os_release and re.search('Ubuntu', os_release):
        print(f'OS Ubuntu')
        packages = ''
        packages += f'ascii aview imagemagick '
        packages += f'cmatrix figlet hollywood '
        packages += f'fortunes fortunes-zh cowsay lolcat '

        cmd = f'sudo -E apt install -y ' + packages
        exec_bash(cmd)
    else:
        raise RuntimeError(f'Unsupported OS {os_release}')


def install_vim_configure(dst):
    config = pathlib.Path().resolve().joinpath('configs/vimrc')
    if not config.exists():
        raise RuntimeError(f'File does not exist, {config}')

    dst_config = dst.joinpath('.vimrc')
    dst_config.unlink(missing_ok=True)
    dst_config.symlink_to(config)
    print(f'{dst_config} -> {config}')

    # clone
    git_dst = dst.joinpath('.vim/bundle/vundle')
    if git_dst.exists():
        os.chdir(str(git_dst))

        cmd = f'git fetch'
        exec_bash(cmd, shell=True)
        cmd = f'git rebase'
        exec_bash(cmd, shell=True)
    else:
        cmd = f'git clone git@github.com:gmarik/vundle.git {git_dst}'
        exec_bash(cmd)

    cmd = 'vim +PluginInstall +qall'
    exec_bash(cmd)

    return


def install_git_configure(dst):
    config = pathlib.Path().resolve().joinpath('configs/gitconfig')
    if not config.exists():
        raise RuntimeError(f'File does not exist, {config}')

    dst_config = dst.joinpath('.gitconfig')
    dst_config.unlink(missing_ok=True)
    dst_config.symlink_to(config)
    print(f'{dst_config} -> {config}')

    return


def install_tmux_configure(dst):
    config = pathlib.Path().resolve().joinpath('configs/tmux.conf')
    if not config.exists():
        raise RuntimeError(f'File does not exist, {config}')

    dst_config = dst.joinpath('.tmux.conf')
    dst_config.unlink(missing_ok=True)
    dst_config.symlink_to(config)
    print(f'{dst_config} -> {config}')

    return


def main() -> int:
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument('-r',
                        '--root',
                        dest='root',
                        action='store',
                        default=None,
                        help="Set root install path")
    parser.add_argument('-a',
                        '--all',
                        dest='install_all',
                        action='store_true',
                        default=False,
                        help="Install all")
    parser.add_argument('-d',
                        '--deps',
                        dest='install_deps',
                        action='store_true',
                        default=False,
                        help="Install all deps")
    parser.add_argument('--vim',
                        dest='install_vim',
                        action='store_true',
                        default=False,
                        help="Install vim config")
    parser.add_argument('--git',
                        dest='install_git',
                        action='store_true',
                        default=False,
                        help="Install git config")
    parser.add_argument('--tmux',
                        dest='install_tmux',
                        action='store_true',
                        default=False,
                        help="Install tmux config")
    args = parser.parse_args()

    # set pwd
    pwd = pathlib.Path().resolve()
    if args.root:
        pwd = pathlib.Path(args.root).resolve()
    print(f'Set dst, {pwd}')

    # install deps
    if args.install_deps or args.install_all:
        install_deps()

    if args.install_git or args.install_all:
        install_git_configure(pwd)

    if args.install_tmux or args.install_all:
        install_tmux_configure(pwd)

    if args.install_vim or args.install_all:
        install_vim_configure(pwd)

    print('Done')
    return 0


if __name__ == '__main__':
    sys.exit(main())
