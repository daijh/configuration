##!/bin/bash -ex

THIS=$(realpath $(pwd)/$BASH_SOURCE)
if [ ! -f ${THIS} ]; then
  THIS=$(realpath $BASH_SOURCE)
fi
CURRENT=$(dirname ${THIS})

PREFIX=~/third_party/nfs/chromium-linux/src/out/Default/

CODEC="vp9"
BITRATE=2250000
LOG=vea_tests.log

INPUT_DIR=~/third_party/test_streams/vp9_lossless_static
INPUT_YUV=youtube_screenshot_static.webm
INPUT=${INPUT_DIR}/${INPUT_YUV}

rm VideoEncoderTest -rf

CMD="${PREFIX}/video_encode_accelerator_tests \
  --codec=${CODEC} \
  --bitrate=${BITRATE} \
  --output_bitstream ${INPUT} \
  --gtest_filter=VideoEncoderTest.FlushAtEndOfStream \
  --vmodule=*/media/gpu/*=4 \
"

${CMD} |& tee ${LOG}

echo ""
echo "PREFIX: ${PREFIX}"
echo "INPUT: ${INPUT}"
echo "${CMD}"
