#!/bin/sh

#if [ $# -ne 1 ] 
#then
#    echo "Usage: $0 outputFolder"
#    return
#fi

mediaserver_pid=`adb shell ps | grep mediaserver | awk '{print \$2}'`
surfaceflinger_pid=`adb shell ps | grep surfaceflinger| awk '{print $2}'`

adb shell ps | egrep "mediaserver|surfaceflinger"
echo "mediaserver pid is $mediaserver_pid"
echo "surfaceflinger pid is $surfaceflinger_pid"

adb shell procmem $mediaserver_pid > ./mediaserver-procmem.txt
adb shell procmem $surfaceflinger_pid > ./surfaceflinger-procmem.txt

awk '/heap|malloc/ {print $0;vss_sum += $1;pss_sum += $3 };END {print "media heap vss is:", vss_sum, "pss is: ", pss_sum}' ./mediaserver-procmem.txt
awk '/heap|malloc/ {print $0;vss_sum += $1;pss_sum += $3 };END {print "sf heap vss is:", vss_sum, "pss is: ", pss_sum}' ./surfaceflinger-procmem.txt
