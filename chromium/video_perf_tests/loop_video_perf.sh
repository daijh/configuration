#!/bin/bash -ex

loop=3

#dec_test_stream=data/test-25fps.h264
#enc_test_stream=data/bear_320x192_40frames.yuv.webm

dec_test_stream=data/1280x720-100frames-h264.h264
enc_test_stream=data/1280x720-100frames-vp9.webm

counter=1
while [[ $counter -le loop ]]; do
	echo "Loop: $counter"
	./run_video_perf.sh -d ${dec_test_stream}
	./run_video_perf.sh -e ${enc_test_stream}

	mv perf_metrics perf_metrics-lock-$counter
	((counter++))
done

counter=1
while [[ $counter -le loop ]]; do
	echo "Loop: $counter"
	./run_video_perf.sh -d ${dec_test_stream} --disable_vaapi_lock
	./run_video_perf.sh -e ${enc_test_stream} --disable_vaapi_lock

	mv perf_metrics perf_metrics-nolock-$counter
	((counter++))
done
