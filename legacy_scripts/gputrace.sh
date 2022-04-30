#!/bin/bash

SYSTRACE=""

startSystrace()
{
#adb shell "echo 0 > /sys/kernel/debug/tracing/events/irq/enable"
#adb shell "echo 0 > /sys/kernel/debug/tracing/events/power/enable"
#adb shell "echo 0 > /sys/kernel/debug/tracing/events/timer/enable"

adb shell "echo 1 > /sys/kernel/debug/tracing/events/drm/tracing_mark_write/enable"
#adb shell "echo 1 > /sys/kernel/debug/tracing/events/i915/i915_flip_request/enable"
#adb shell "echo 1 > /sys/kernel/debug/tracing/events/i915/i915_flip_complete/enable"

    #python systrace.py --cpu-freq --cpu-load -s -w --time=20 -b 102400 -o $1
    python systrace.py --time=10 -b 80000 gfx video sched -o $1
    #python systrace.py --time=7 -b 50000 gfx video -o $1
}

stopSystrace()
{
adb shell "echo 0 > /sys/kernel/debug/tracing/events/drm/tracing_mark_write/enable"
#adb shell "echo 0 > /sys/kernel/debug/tracing/events/i915/i915_flip_request/enable"
#adb shell "echo 0 > /sys/kernel/debug/tracing/events/i915/i915_flip_complete/enable"

	echo "systrace stoped"
}

startMVP()
{
    adb shell "rm /data/Perf_Data_*"

	MVPDIR=`adb shell ls -d /data/mvp_data`
	if [ $MVPDIR == "" ]; then
		adb shell mkdir /data/mvp_data
	fi

	MVPDATA=`adb shell "cd /data && ls Perf_Data*data"`
	if [[ ! "$MVPDATA" =~ "No such file or directory" ]]; then
		adb shell mv /data/Perf_Data*data /data/mvp_data
	fi

	MVPPID=`adb shell ps |grep MVP_Agent |grep -v grep | awk '{print $2}'`
	if [ "$MVPPID" != "" ]; then
		echo "MVP is already runing!"
	else
		adb shell /system/bin/MVP_Agent&
		echo "MVP is started successfully!"
	fi
	adb shell "echo on > /proc/mvp/mvp_switch"
}

stopMVP()
{
	adb shell "echo off > /proc/mvp/mvp_switch"
	MVPPID=`adb shell ps |grep MVP_Agent |grep -v grep | awk '{print $2}'`
	if [ "$MVPPID" == "" ]; then
		echo "MVP is already stopped!"
	else
		adb shell kill -9 $MVPPID
		echo "MVP is stopped successfully!"
	fi
	
}

mergeData()
{
	
	#MVPDATA=`adb shell "cd /data/ && find ./ -maxdepth 1 -name Perf_Data* -print0 | xargs -0"`
	MVPDATA=`adb shell "cd /data/ && busybox ls -ltr Perf_Data*"|tail -1|awk '{print $9}'`
	if [ "$MVPDATA" == "" ]; then
		echo "No mvp data produced, please check if MVP is installed correctly"
		exit
	else
		MVPDATA=`echo $MVPDATA | sed 's/.*\(Perf_Data.*data\).*/\1/'`
		adb pull /data/${MVPDATA}
	fi
	if [ ! -d /tmp/mvp_data ]; then
		mkdir /tmp/mvp_data
	fi
	LINENUM=`wc -l $SYSTRACE | awk '{print $1}'`
	TRACEEND=`expr $LINENUM \- 5`
	sed -n -e "1, ${TRACEEND}p" $SYSTRACE > /tmp/systrace.html
	mvp-trace ${MVPDATA}>> /tmp/systrace.html
	TRACESUFFIX=`expr $LINENUM \- 4`
	sed -n -e "${TRACESUFFIX}, ${LINENUM}p" $SYSTRACE >> /tmp/systrace.html
	mv Perf_Data_*data /tmp/mvp_data
	mv Perf_Data_*bin /tmp/mvp_data
	cp /tmp/systrace.html $SYSTRACE
}

main()
{
	if [ $# -ne 1 ]; then
		echo "Usage: ./gputrace.sh sample.html"
		return
	fi
	SYSTRACE=$1
	startMVP
	startSystrace $1
	stopMVP
	stopSystrace
	mergeData
}

main $1
