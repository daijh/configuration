#!/bin/bash
THIS=$(realpath $0)
if [ ! -f ${THIS} ]; then
  THIS=$0
fi

ROOT=$(dirname ${THIS})

install_deps_for_dev() {
  sudo -E apt install -y apt-file git tig exuberant-ctags tmux tree ack-grep vim build-essential automake global cmake libtool
  sudo -E apt install -y curl ssh samba cifs-utils nfs-common nfs-kernel-server gnome-remote-desktop
  sudo -E apt install -y lm-sensors cpuid cpuinfo hwloc

  sudo -E apt install -y shfmt cmake-format

  sudo -E apt install -y nodejs npm
  #sudo -E npm install -g --save-dev --save-exact prettier
}

install_deps_others() {
  sudo -E apt install -y ascii aview imagemagick
  sudo -E apt install -y cmatrix figlet hollywood
  sudo -E apt install -y fortunes fortunes-zh cowsay lolcat
}

source /etc/os-release
if [ $NAME != "Ubuntu" ]; then
  echo "Unsupported OS: ${NAME}"
  exit
fi

install_deps_for_dev
install_deps_others
