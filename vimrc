
" ===Common Setting===
colorscheme delek

syntax on
filetype plugin indent on
let mapleader = ","
set ignorecase
set incsearch
set nonumber
set nocompatible " not compatible w/ vi
set cursorline " highlight current line

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
"autocmd FileType c,cpp setlocal tabstop=2 softtabstop=2 shiftwidth=2
" linux kernel
"autocmd FileType c,cpp setlocal tabstop=8 softtabstop=8 shiftwidth=8

" gitcommit
autocmd FileType gitcommit setlocal tw=72 cc=+1 spell

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

" windows manager
Plugin 'minibufexpl.vim'

let g:miniBufExplorerMoreThanOne=1
" let g:miniBufExplModSelTarget = 1
" let g:miniBufExplForceSyntaxEnable = 1
let g:miniBufExplMapWindowNavVim = 1
let g:miniBufExplMapWindowNavArrows = 1
let g:miniBufExplMapCTabSwitchBufs = 1
let g:miniBufExplModSelTarget = 1

" code tags
Plugin 'majutsushi/tagbar'

nmap tl :TagbarToggle
let g:tagbar_left=1

" find files (TODO)
Plugin 'kien/ctrlp.vim'

" easy motion (TODO)
Plugin 'Lokaltog/vim-easymotion'

" mark words
Plugin 'Mark'

" status/tabline
Plugin 'vim-airline/vim-airline'

" grep
" Plugin 'grep.vim'
"
" nnoremap <silent> <F6> :Grep<CR>
" nnoremap <silent> <F7> :Bgrep<CR>

" ack
Plugin 'mileszs/ack.vim'

nnoremap <silent> <F7> :Ack<CR>

" as name
Plugin 'ShowTrailingWhitespace'

" mark
Plugin 'kshenoy/vim-signature'

" markdown preview (TODO)

" Install vim-codefmt and its dependencies
Plugin 'google/vim-maktaba'
Plugin 'google/vim-codefmt'
" Also add Glaive, which is used to configure codefmt's maktaba flags. See
" " `:help :Glaive` for usage.
Plugin 'google/vim-glaive'
" " ...
Plugin 'https://gn.googlesource.com/gn', { 'rtp': 'misc/vim' }

call vundle#end()
" " the glaive#Install() should go after the "call vundle#end()"
"call glaive#Install()

" Optional: configure vim-codefmt to autoformat upon saving the buffer.
augroup CodeFmt
    autocmd!
    "autocmd FileType gn AutoFormatBuffer gn
    "autocmd FileType c,cpp,proto,javascript,arduino AutoFormatBuffer clang-format
    " Other file types...
augroup END
