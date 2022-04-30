#!/bin/bash

ALL_TESTS=false
if [[ $2 == "-a" ]]; then
  ALL_TESTS=true
fi

PREFIX=./src/out/Default
LOG_DIR=./pacer_test_results

rm -rf $LOG_DIR
mkdir -p $LOG_DIR

${PREFIX}/modules_unittests |& tee ${LOG_DIR}/my-modules_unittests.log &
${PREFIX}/peerconnection_unittests |& tee ${LOG_DIR}/my-peerconnection_unittests.log &
${PREFIX}/test_support_unittests |& tee ${LOG_DIR}/my-test_support_unittests.log &
${PREFIX}/low_bandwidth_audio_test |& tee ${LOG_DIR}/my-low_bandwidth_audio_test.log &
${PREFIX}/video_engine_tests |& tee ${LOG_DIR}/my-video_engine_tests.log &
${PREFIX}/voip_unittests |& tee ${LOG_DIR}/my-voip_unittests.log &
${PREFIX}/rtc_unittests |& tee ${LOG_DIR}/my-rtc_unittests.log &
${PREFIX}/rtc_media_unittests |& tee ${LOG_DIR}/my-rtc_media_unittests.log &

if [ ${ALL_TESTS} == "true" ]; then
  ${PREFIX}/webrtc_perf_tests |& tee ${LOG_DIR}/my-webrtc_perf_tests.log &
fi

wait

grep FAILED $LOG_DIR/*
