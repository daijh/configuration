#!/bin/bash

THIS=$(realpath $0)
if [ ! -f ${THIS} ]; then
  THIS=$0
fi

CURRENT=$(dirname ${THIS})
OUTPUT_DIR=video_enc_perf_result

rm -rf ${OUTPUT_DIR}

function RunEncPerfTests() {
  logging=$2
  vaapi_lock=$1

  test_resolutions=(
    320x180
    640x360
    1280x720
  )
  for resolution in "${test_resolutions[@]}"; do
    test_stream_dir=test_streams/bbb_enc_test_streams
    test_stream=${test_stream_dir}/bbb_${resolution}_vp9-100frames.webm

    program="src/out/Default/video_encode_accelerator_perf_tests \
--gtest_filter=*MeasureUncappedPerformance_MultipleConcurrentEncoders* \
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
RunEncPerfTests true false
RunEncPerfTests false false

find ${OUTPUT_DIR} -type f | sort | xargs grep FPS
