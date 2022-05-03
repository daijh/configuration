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
fi

# git
echo -e "[include]\n\tpath = ${ROOT}/gitconfig" >> ~/.gitconfig

# tmux
ln -s -v ${ROOT}/tmux.conf ~/.tmux.conf

${ROOT}/install_vim.sh
