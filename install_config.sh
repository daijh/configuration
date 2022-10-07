#!/bin/bash
THIS=$(realpath $0)
if [ ! -f ${THIS} ]; then
  THIS=$0
fi

ROOT=$(dirname ${THIS})

# git
echo -e "[include]\n\tpath = ${ROOT}/gitconfig" >> ~/.gitconfig

# tmux
ln -s -v ${ROOT}/tmux.conf ~/.tmux.conf

${ROOT}/install_vim.sh
