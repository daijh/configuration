#!/bin/bash

THIS=`pwd`/$0
if [ ! -f ${THIS} ]; then
    THIS=$0
fi
ROOT=`dirname ${THIS}`

source /etc/os-release
if [ $NAME = "Ubuntu" ]; then
    sudo -E apt install -y git exuberant-ctags tmux tree ack-grep vim ssh \
samba build-essential automake global cmake
    sudo -E apt install -y lm-sensors cpuid cpuinfo hwloc
    sudo -E apt install -y ascii aview imagemagick
    sudo -E apt install -y cmatrix figlet hollywood
    sudo -E apt install -y fortunes fortunes-zh cowsay lolcat
else
    sudo -E yum install -y git exuberant-ctags tmux tree ack-grep vim ssh samba \
build-essential automake
fi

# vim
echo -e "source ${ROOT}/vimrc" >> ~/.vimrc

git clone https://github.com/gmarik/vundle.git ~/.vim/bundle/vundle
vim +PluginInstall +qall

# git
echo -e "[include]\n\tpath = ${ROOT}/gitconfig" >> ~/.gitconfig

# tmux
ln -s -v ${ROOT}/tmux.conf ~/.tmux.conf

