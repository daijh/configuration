#!/bin/bash

THIS=$(realpath $0)
if [ ! -f ${THIS} ]; then
  THIS=$0
fi

CURRENT=$(dirname ${THIS})
OUTPUT_DIR=video_dec_perf_result

rm -rf ${OUTPUT_DIR}

function RunDecPerfTests() {
  logging=$2
  vaapi_lock=$1

  test_resolutions=(
    320x180
    640x360
    1280x720
  )
  for resolution in "${test_resolutions[@]}"; do
    test_stream_dir=test_streams/bbb_dec_test_streams
    #test_stream=${test_stream_dir}/bbb-$resolution-40frames.h264
    test_stream=${test_stream_dir}/bbb-$resolution-100frames.h264
    #test_stream=${test_stream_dir}/bbb-$resolution-10890frames.h264

    program="src/out/Default/video_decode_accelerator_perf_tests \
--gtest_filter=*MeasureUncappedPerformance_TenConcurrentDecoders* \
$test_stream"

    if [ ${vaapi_lock} == "false" ]; then
      program="$program --disable_vaapi_lock"
    fi

    if [ ${logging} == "true" ]; then
      program="$program --vmodule=*/ozone/*=4,*/wayland/*=4,*/vaapi/*=4,*/media/*=0,*/viz/*=4"
    fi

    i=0
    while [ $i -lt 1 ]; do
      echo "Loop $i : $program"
      $program |& tee ./out.log

      dest=${OUTPUT_DIR}/lock-$1/$resolution-$i
      mkdir -p $dest
      mv out.log $dest
      #mv perf_metrics $dest

      ((i++))
    done

  done
}

#params: vaapi_lock logging
RunDecPerfTests true false
RunDecPerfTests false false

find ${OUTPUT_DIR} -type f | sort | xargs grep FPS
