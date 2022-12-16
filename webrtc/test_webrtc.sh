#!/bin/bash
##!/bin/bash -ex

ALL_TESTS=false
if [[ $2 == "-a" ]]; then
  ALL_TESTS=true
fi

PREFIX=./src/out/Default
LOG_DIR=./test_results

rm -rf $LOG_DIR
mkdir -p $LOG_DIR

ALL_TEST_CASES=(
  webrtc_perf_tests
  rtc_pc_unittests
  slow_peer_connection_unittests
  test_support_unittests
  fuchsia_perf_tests
  modules_unittests
  svc_tests
  video_engine_tests
  rtc_unittests
  webrtc_lib_link_test
  low_bandwidth_audio_test
)

if [[ $# -gt 0 ]]; then
  TEST_CASES=$@
else
  TEST_CASES=${ALL_TEST_CASES[@]}
fi

for case in "${TEST_CASES[@]}"; do
  echo "Run ${case}"
  ${PREFIX}/${case} |& tee ${LOG_DIR}/${case}.log &
done

wait

echo "++++++"
echo "***All Tests Done!***"
echo "------"
grep -E "PASSED|FAILED" $LOG_DIR/*
