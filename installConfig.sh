#~/bin/sh

CURRENT_DIR=`pwd`

# vim
echo -e "source $CURRENT_DIR/vimrc" >> ~/.vimrc

git clone https://github.com/gmarik/vundle.git ~/.vim/bundle/vundle
vim +PluginInstall +qall

#alias vimtags='(echo "!_TAG_FILE_SORTED    2   /2=foldcase/"; \
#	(find . \( -name .svn -o -name .repo -o -name .git \) -prune -o -type f -printf "%f\t%p\t1\n" | \
#	sort -f)) > ./filenametags; gtags -i'

# git
echo -e "[include]\n\tpath = $CURRENT_DIR/gitconfig" >> ~/.gitconfig

# tmux
ln -s -v $CURRENT_DIR/tmux.conf ~/.tmux.conf

