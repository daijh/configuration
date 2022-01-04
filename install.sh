#!/bin/bash

THIS=`pwd`/$0
if [ ! -f ${THIS} ]; then
    THIS=$0
fi
ROOT=`dirname ${THIS}`

source /etc/os-release
if [ $NAME = "Ubuntu" ]; then
    sudo -E apt install -y git exuberant-ctags tmux tree ack-grep vim ssh \
samba build-essential automake global cmake lm-sensors cmatrix
    sudo -E apt install -y lm-sensors ascii -y
    sudo -E apt install -y aview imagemagick -y
    sudo -E apt install -y cmatrix figlet hollywood -y
    sudo -E apt install -y fortunes fortunes-zh cowsay lolcat -y
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

