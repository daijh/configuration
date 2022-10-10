#!/bin/bash
THIS=$(realpath $0)
if [ ! -f ${THIS} ]; then
  THIS=$0
fi

ROOT=$(dirname ${THIS})

source /etc/os-release
if [ $NAME = "Ubuntu" ]; then
    sudo -E apt install -y apt-file
    sudo -E apt install -y git tig exuberant-ctags tmux tree ack-grep vim ssh \
samba cifs-utils build-essential automake global cmake libtool
    sudo -E apt install -y lm-sensors cpuid cpuinfo hwloc
    sudo -E apt install -y ascii aview imagemagick
    sudo -E apt install -y cmatrix figlet hollywood
    sudo -E apt install -y fortunes fortunes-zh cowsay lolcat
    sudo -E apt install -y nfs-common gnome-remote-desktop

    sudo -E apt install -y shfmt cmake-format
    sudo -E apt install -y nodejs npm
    sudo -E npm install -g --save-dev --save-exact prettier
fi
