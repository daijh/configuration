#~/bin/sh
ln -s -v ~/configuration/vimrc ~/.vimrc
ln -s -v ~/configuration/tmux.conf ~/.tmux.conf
echo -e "[include]\n\tpath = ~/configuration/gitconfig" >> ~/.gitconfig

git clone https://github.com/gmarik/vundle.git ~/.vim/bundle/vundle
vim +PluginInstall +qall


#alias vimtags='(echo "!_TAG_FILE_SORTED    2   /2=foldcase/"; \
#	(find . \( -name .svn -o -name .repo -o -name .git \) -prune -o -type f -printf "%f\t%p\t1\n" | \
#	sort -f)) > ./filenametags; gtags -i'
