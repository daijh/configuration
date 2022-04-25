#!/bin/bash

if [ $# -lt 1 ]; then
	echo "Usage: $0 link_file_list"
	exit
fi

DRY_RUN=false
if [[ $2 == "-m" ]]; then
	DRY_RUN=true
fi
echo "DRY_RUN: ${DRY_RUN}"

LINK_FILES=$1

while IFS= read -r line; do
	#echo "$line"
	link_name=$(echo "$line" | awk -F@ '{print $1}')
	target=$(echo "$line" | awk -F@ '{print $2}')
	#echo "target: $target"
	#echo "link_name: $link_name"
	if [ ${DRY_RUN} == "true" ]; then
		rm $link_name
		ln -s -v ${target} ${link_name}
	else
		echo "dry run: ${link_name} --> ${target}"
	fi

done <"$LINK_FILES"
