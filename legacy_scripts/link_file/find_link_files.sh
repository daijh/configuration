#!/bin/bash

if [ $# -ne 1 ]; then
	echo "Usage: $0 output"
	exit
fi

LINK_FILES=$(find -type l -print)
OUTPUT=$1

>${OUTPUT}
for FILE in ${LINK_FILES}; do
	TARGET=$(readlink ${FILE})
	echo "${FILE}@${TARGET}" >>${OUTPUT}
done

count=$(wc -l ${OUTPUT})

echo "Find ${count} link files in $(pwd), result writed in ${OUTPUT}"

#ln -s -v target link_name

#link name
#awk -F@ '{print $1}' ${OUTPUT}

#target
#awk -F@ '{print $2}' ${OUTPUT}
