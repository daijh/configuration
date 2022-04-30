#!/bin/sh

if [ $# -ne 1 ]
then
    echo "Usage: $0 path"
    return
fi

filelist=`ls $1`

for file in $filelist
do
    if test -d $1/$file
    then
		echo "++++++++++++"$file"++++++++++++"
		cd $file
		/home/jdai12/bin/script/mem-ppc.sh
		cd -
    fi
done

