
alias diffc='colordiff'
alias ascii='man ascii'
alias mediascanAndroid='adb shell am broadcast -a android.intent.action.MEDIA_MOUNTED -d file:///sdcard/Movies'
alias pythoncompile='python /usr/share/doc/python2.7/examples/Tools/freeze/freeze.py '
alias vimtags='(echo "!_TAG_FILE_SORTED    2   /2=foldcase/"; \
	        (find . \( -name .svn -o -name .repo -o -name .git \) -prune -o -type f -printf "%f\t%p\t1\n" | \
			        sort -f)) > ./filenametags; gtags -i'
