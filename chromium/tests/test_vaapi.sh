#!/bin/bash -ex

ALL_TESTS=false
if [[ $2 == "-a" ]]; then
	ALL_TESTS=true
fi

PREFIX=./src/out/Default
LOG_DIR=./vaapi_test_results

rm -rf $LOG_DIR
mkdir -p $LOG_DIR

${PREFIX}/media_unittests --gtest_filter=*Vaapi* |& tee ${LOG_DIR}/my-media_unittests.log &
${PREFIX}/vaapi_unittest |& tee ${LOG_DIR}/my-vaapi_unittest.log &

# need test data, codec setting
#${PREFIX}/video_decode_accelerator_tests |& tee ${LOG_DIR}/my-video_decode_accelerator_tests.log &
#${PREFIX}/video_encode_accelerator_tests |& tee ${LOG_DIR}/my-video_encode_accelerator_tests.log &
#${PREFIX}/video_decode_accelerator_perf_tests |& tee ${LOG_DIR}/my-video_decode_accelerator_tests.log &
#${PREFIX}/video_encode_accelerator_perf_tests |& tee ${LOG_DIR}/my-video_encode_accelerator_tests.log &

wait

grep -E "PASSED|FAILED" $LOG_DIR/*
