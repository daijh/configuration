#!/usr/bin/python3 -u

import sys
import os
import re
import pathlib
import subprocess
import argparse
import shutil


def run_shell(cmd, check=True, env=None, log_file=None, shell=False):
    print(f'{cmd}\n')

    if log_file:
        print(f'Write log: {log_file}\n')

        result = subprocess.run(cmd.split(),
                                check=check,
                                env=env,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                shell=shell,
                                text=True)
        with open(log_file, 'w', encoding="utf-8") as f:
            f.write(result.stdout)
    else:
        result = subprocess.run(cmd.split(), check=check, env=env)

    result.stdout = None
    print(f'{result}\n')
    return result


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
        run_shell(cmd, check=False)
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
        run_shell(cmd)
    else:
        raise RuntimeError(f'Unsupported OS {os_release}')


def install_vim_configure(home_dir):
    config = pathlib.Path().resolve().joinpath('configs/vimrc')
    if not config.exists():
        raise RuntimeError(f'File does not exist, {config}')

    dst_config = home_dir.joinpath('.vimrc')
    dst_config.unlink(missing_ok=True)
    dst_config.symlink_to(config)
    print(f'{dst_config} -> {config}')

    # clone
    git_dst = home_dir.joinpath('.vim/bundle/vundle')
    if git_dst.exists():
        os.chdir(str(git_dst))

        cmd = f'git fetch'
        run_shell(cmd, shell=True)
        cmd = f'git rebase'
        run_shell(cmd, shell=True)
    else:
        cmd = f'git clone git@github.com:gmarik/vundle.git {git_dst}'
        run_shell(cmd)

    cmd = 'vim +PluginInstall +qall'
    run_shell(cmd)

    return


def install_git_configure(home_dir):
    config = pathlib.Path().resolve().joinpath('configs/gitconfig')
    if not config.exists():
        raise RuntimeError(f'File does not exist, {config}')

    dst_config = home_dir.joinpath('.gitconfig')
    dst_config.unlink(missing_ok=True)
    dst_config.symlink_to(config)
    print(f'{dst_config} -> {config}')

    return


def install_tmux_configure(home_dir):
    config = pathlib.Path().resolve().joinpath('configs/tmux.conf')
    if not config.exists():
        raise RuntimeError(f'File does not exist, {config}')

    dst_config = home_dir.joinpath('.tmux.conf')
    dst_config.unlink(missing_ok=True)
    dst_config.symlink_to(config)
    print(f'{dst_config} -> {config}')

    return


def main() -> int:
    parser = argparse.ArgumentParser(allow_abbrev=False)
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

    # set home dir
    home_dir = pathlib.Path('~').expanduser()
    this_dir = pathlib.Path(__file__).resolve().parent

    # install deps
    if args.install_deps or args.install_all:
        install_deps()

    if args.install_git or args.install_all:
        install_git_configure(home_dir)

    if args.install_tmux or args.install_all:
        install_tmux_configure(home_dir)

    if args.install_vim or args.install_all:
        install_vim_configure(home_dir)

    print('Done')
    return 0


if __name__ == '__main__':
    sys.exit(main())
