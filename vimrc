" common
:syntax on
filetype plugin on
let mapleader = ","
set ignorecase
set incsearch
set nonumber
" set number

set smarttab
set tabstop=4
set shiftwidth=4
" set expandtab
" set autoindent
" set ai!
" common end

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

" cscope
if has("cscope")
	set cscopequickfix=s-,c-,d-,i-,t-,e-
	" set csprg=/usr/local/bin/cscope
	set csprg=gtags-cscope
	set csto=0
	" set cst
	set nocst
	set nocsverb

	let db = findfile("GTAGS", ".;")
	if (!empty(db))
	    if (db == "GTAGS")
		let path = getcwd()
	    else
	        let path = strpart(db, 0, match(db, "/GTAGS$"))
	    endif

	    exe "cs add " . db . " " . path
	endif

	set csverb

	"nmap <leader>s :cs find s <C-R>=expand("<cword>")<CR><CR>
	"nmap <leader>g :cs find g <C-R>=expand("<cword>")<CR><CR>
	"nmap <leader>c :cs find c <C-R>=expand("<cword>")<CR><CR>
	"nmap <leader>t :cs find t <C-R>=expand("<cword>")<CR><CR>
	"nmap <leader>e :cs find e <C-R>=expand("<cword>")<CR><CR>
	"nmap <leader>f :cs find f <C-R>=expand("<cfile>")<CR><CR>
	"nmap <leader>i :cs find i ^<C-R>=expand("<cfile>")<CR>$<CR>
	"nmap <leader>d :cs find d <C-R>=expand("<cword>")<CR><CR>

	"nmap <C-_>s :cs find s <C-R>=expand("<cword>")<CR><CR>
	"nmap <C-_>g :cs find g <C-R>=expand("<cword>")<CR><CR>
	"nmap <C-_>c :cs find c <C-R>=expand("<cword>")<CR><CR>
	"nmap <C-_>t :cs find t <C-R>=expand("<cword>")<CR><CR>
	"nmap <C-_>e :cs find e <C-R>=expand("<cword>")<CR><CR>
	"nmap <C-_>f :cs find f <C-R>=expand("<cfile>")<CR><CR>
	"nmap <C-_>i :cs find i ^<C-R>=expand("<cfile>")<CR>$<CR>
	"nmap <C-_>d :cs find d <C-R>=expand("<cword>")<CR><CR>

	" Using 'CTRL-spacebar' then a search type makes the vim window
	" split horizontally, with search result displayed in
	" the new window.

	"nmap <C-Space>s :scs find s <C-R>=expand("<cword>")<CR><CR>
	"nmap <C-Space>g :scs find g <C-R>=expand("<cword>")<CR><CR>
	"nmap <C-Space>c :scs find c <C-R>=expand("<cword>")<CR><CR>
	"nmap <C-Space>t :scs find t <C-R>=expand("<cword>")<CR><CR>
	"nmap <C-Space>e :scs find e <C-R>=expand("<cword>")<CR><CR>
	"nmap <C-Space>f :scs find f <C-R>=expand("<cfile>")<CR><CR>
	"nmap <C-Space>i :scs find i ^<C-R>=expand("<cfile>")<CR>$<CR>
	"nmap <C-Space>d :scs find d <C-R>=expand("<cword>")<CR><CR>

	" Hitting CTRL-space *twice* before the search type does a vertical
	" split instead of a horizontal one

	"nmap <C-Space><C-Space>s
	"	\:vert scs find s <C-R>=expand("<cword>")<CR><CR>
	"nmap <C-Space><C-Space>g
	"	\:vert scs find g <C-R>=expand("<cword>")<CR><CR>
	"nmap <C-Space><C-Space>c
	"	\:vert scs find c <C-R>=expand("<cword>")<CR><CR>
	"nmap <C-Space><C-Space>t
	"	\:vert scs find t <C-R>=expand("<cword>")<CR><CR>
	"nmap <C-Space><C-Space>e
	"	\:vert scs find e <C-R>=expand("<cword>")<CR><CR>
	"nmap <C-Space><C-Space>i
	"	\:vert scs find i ^<C-R>=expand("<cfile>")<CR>$<CR>
	"nmap <C-Space><C-Space>d
	"	\:vert scs find d <C-R>=expand("<cword>")<CR><CR>
endif
" cscope end

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
Bundle 'cscope.vim'

Bundle 'L9'
Bundle 'FuzzyFinder'

Bundle 'genutils'
Bundle 'lookupfile'
