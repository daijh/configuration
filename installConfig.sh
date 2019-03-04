#~/bin/sh

CURRENT_DIR=`pwd`

# vim
echo -e "source $CURRENT_DIR/vimrc" >> ~/.vimrc

git clone https://github.com/gmarik/vundle.git ~/.vim/bundle/vundle
vim +PluginInstall +qall

# git
echo -e "[include]\n\tpath = $CURRENT_DIR/gitconfig" >> ~/.gitconfig

# tmux
ln -s -v $CURRENT_DIR/tmux.conf ~/.tmux.conf

