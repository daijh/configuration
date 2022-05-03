#!/bin/bash

THIS=`pwd`/$0
if [ ! -f ${THIS} ]; then
    THIS=$0
fi
ROOT=`dirname ${THIS}`

# vim
echo -e "source ${ROOT}/vimrc" >> ~/.vimrc

git clone git@github.com:gmarik/vundle.git ~/.vim/bundle/vundle
vim +PluginInstall +qall

