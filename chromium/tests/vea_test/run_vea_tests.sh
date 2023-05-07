##!/bin/bash -ex

THIS=$(realpath $(pwd)/$BASH_SOURCE)
if [ ! -f ${THIS} ]; then
  THIS=$(realpath $BASH_SOURCE)
fi
CURRENT=$(dirname ${THIS})

PREFIX=~/third_party/nfs/chromium-linux/src/out/Default/

LOG=vea_tests.log

#CODEC="vp9"
#BITRATE=2250000
#INPUT_DIR=~/third_party/test_streams/vp9_lossless_static
#INPUT_YUV=youtube_screenshot_static.webm

# pc_full_stack_tests.cc - Chromium Code Search
# https://source.chromium.org/chromium/chromium/src/+/main:third_party/webrtc/video/pc_full_stack_tests.cc;l=1268?q=1500&ss=chromium%2Fchromium%2Fsrc:third_party%2Fwebrtc%2F

# 720p
CODEC="vp9"
BITRATE=1500000
INPUT_DIR=~/Videos/gipsrestat
INPUT_YUV=gipsrestat-1280x720_20210211.vp9.webm
# 360
CODEC="vp9"
BITRATE=500000
INPUT_DIR=~/Videos/gipsrestat
INPUT_YUV=gipsrestat-640x360_20210211.vp9.webm
# 180
CODEC="vp9"
BITRATE=150000
INPUT_DIR=~/Videos/gipsrestat
INPUT_YUV=gipsrestat-320x180_20210211.vp9.webm

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
