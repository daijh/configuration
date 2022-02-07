
" ===Common Setting===
colorscheme delek

syntax on
filetype plugin on
let mapleader = ","
set ignorecase
set incsearch
set nonumber
set nocompatible " not compatible w/ vi

" ===foldenable===
"set nofoldenable
"set foldenable
"set foldmethod=syntax
"set foldmethod=manual
" ===foldenable end===

" normal file type
set tabstop=4 softtabstop=4 shiftwidth=4
set expandtab

" ===Common Setting End===

" ===FileType===
autocmd FileType c,cpp : set foldmethod=syntax
autocmd FileType c,cpp : set nofoldenable
autocmd FileType c,cpp setlocal tw=80
autocmd FileType c,cpp setlocal expandtab

" google
autocmd FileType c,cpp setlocal tabstop=2 softtabstop=2 shiftwidth=2
" linux kernel
"autocmd FileType c,cpp setlocal tabstop=8 softtabstop=8 shiftwidth=8

" gitcommit
autocmd FileType gitcommit setlocal tw=72 cc=+1 spell

" Allow tabs in Makefiles.
autocmd FileType make,automake set noexpandtab shiftwidth=8 softtabstop=8
" ===FileType End===

" vundle
filetype off

set rtp+=~/.vim/bundle/vundle/
call vundle#rc()

" let Vundle manage Vundle
" required!
Bundle 'gmarik/vundle'

" The bundles you install will be listed here

filetype plugin indent on
" vundle end

" NERD Tree
" let NERDChristmasTree=1
" let NERDTreeAutoCenter=1
" let NERDTreeBookmarksFile=$VIM.'\Data\NerdBookmarks.txt'
let NERDTreeMouseMode=2
let NERDTreeShowBookmarks=1
let NERDTreeShowFiles=1
let NERDTreeShowHidden=1
let NERDTreeShowLineNumbers=1
let NERDTreeWinPos='left'
let NERDTreeWinSize=31
" nnoremap f :NERDTreeToggle
" nnoremap c :NERDTreeClose
nmap <leader>f :NERDTreeToggle
" NERD Tree end

" tagbar
nmap tl :TagbarToggle
let g:tagbar_left=1
" tagbar end

" grep
nnoremap <silent> <F6> :Grep<CR>
nnoremap <silent> <F7> :Bgrep<CR>
" grep end

" miniBufExpl
let g:miniBufExplorerMoreThanOne=1
" let g:miniBufExplModSelTarget = 1
" let g:miniBufExplForceSyntaxEnable = 1
let g:miniBufExplMapWindowNavVim = 1
let g:miniBufExplMapWindowNavArrows = 1
let g:miniBufExplMapCTabSwitchBufs = 1
let g:miniBufExplModSelTarget = 1
" miniBufExpl end

" vimdiff
map <silent> <leader>2 :diffget 2<CR> :diffupdate<CR>
map <silent> <leader>3 :diffget 3<CR> :diffupdate<CR>
map <silent> <leader>4 :diffget 4<CR> :diffupdate<CR>
if &diff
    colorscheme evening
    syntax off
endif
" vimdiff end

" The rest of your config follows here

" file explorer
Plugin 'scrooloose/nerdtree'

" windows manager
Plugin 'minibufexpl.vim'

" code tags
Plugin 'majutsushi/tagbar'

" find files (TODO)
Plugin 'kien/ctrlp.vim'

" easy motion
Plugin 'Lokaltog/vim-easymotion'

" mark words
Plugin 'Mark'

" status/tabline
Plugin 'vim-airline/vim-airline'

" regular expression (TODO)
Plugin 'grep.vim'
" Plugin 'mileszs/ack.vim'

" as name
Plugin 'ShowTrailingWhitespace'

" markdown preview (TODO)

