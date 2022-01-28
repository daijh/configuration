" common
colorscheme delek

syntax on
filetype plugin on
let mapleader = ","
set ignorecase
set incsearch
set nonumber
" set number

set tabstop=4 softtabstop=4 shiftwidth=4
set expandtab

" c, cpp
autocmd FileType c,cpp setlocal tw=80
autocmd FileType c,cpp setlocal expandtab

" google
autocmd FileType c,cpp setlocal tabstop=2 softtabstop=2 shiftwidth=2
" linux kernel
"autocmd FileType c,cpp setlocal tabstop=8 softtabstop=8 shiftwidth=8

" gitcommit
autocmd FileType gitcommit setlocal tw=72 cc=+1 spell

" common end

set cindent
set cinoptions=(0
" " Allow tabs in Makefiles.
autocmd FileType make,automake set noexpandtab shiftwidth=8 softtabstop=8
" Trailing whitespace and tabs are forbidden, so highlight them.
highlight ForbiddenWhitespace ctermbg=red guibg=red
match ForbiddenWhitespace /\s\+$\|\t/
" Do not highlight spaces at the end of line while typing on that line.
autocmd InsertEnter * match ForbiddenWhitespace /\t\|\s\+\%#\@<!$/


" diff
if &diff
    colorscheme blue
endif

" vundle
set nocompatible
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

" taglist
let Tlist_Show_One_File=1
let Tlist_Exit_OnlyWindow=1
nmap tl :TlistToggle
" taglist end

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

" gtags
map <C-n> :cn<CR>
map <C-p> :cp<CR>
map <C-\> :GtagsCursor<CR>
" gtags end

" vimdiff
map <silent> <leader>2 :diffget 2<CR> :diffupdate<CR>
map <silent> <leader>3 :diffget 3<CR> :diffupdate<CR>
map <silent> <leader>4 :diffget 4<CR> :diffupdate<CR>
" vimdiff end

" FuzzyFinder
nnoremap <leader>b :FufFile<CR>
" nnoremap <leader>bb :FufBuffer<CR>
" FuzzyFinder end

" lookupfile
let db = findfile("filenametags", ".;")
if (!empty(db))
  let g:LookupFile_TagExpr = string(db)
endif

let g:LookupFile_ignorecase = 1
let g:LookupFile_smartcase = 1
let g:LookupFile_AlwaysAcceptFirst = 1
let g:LookupFile_MinPatLength = 2

function! LookupFile_IgnoreCaseFunc(pattern)
        let _tags = &tags
        try
                let &tags = eval(g:LookupFile_TagExpr)
                let newpattern = '\c' . a:pattern
                let tags = taglist(newpattern)
        catch
                echohl ErrorMsg | echo "Exception: " . v:exception | echohl NONE
                return ""
        finally
                let &tags = _tags
        endtry

        " Show the matches for what is typed so far.
        let files = map(tags, 'v:val["filename"]')
        return files
endfunction
let g:LookupFile_LookupFunc = 'LookupFile_IgnoreCaseFunc'
" lookupfile end

" The rest of your config follows here
Bundle 'scrooloose/nerdtree'
Bundle 'taglist.vim'
Bundle 'grep.vim'
Bundle 'minibufexpl.vim'
Bundle 'Mark'

Bundle 'gtags.vim'

Bundle 'L9'
Bundle 'FuzzyFinder'

Bundle 'genutils'
Bundle 'lookupfile'

Bundle "pangloss/vim-javascript"
