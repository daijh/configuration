##!/bin/bash -ex

THIS=$(realpath $(pwd)/$BASH_SOURCE)
if [ ! -f ${THIS} ]; then
  THIS=$(realpath $BASH_SOURCE)
fi
CURRENT=$(dirname ${THIS})

#PREFIX=$(realpath ${CURRENT}/../src/out/Default/)
PREFIX=${CURRENT}/../src/out/Default/

echo "${PREFIX}"

#data=${CURRENT}/data/staitc-screen-1280x720-300frames.i420.yuv
#data=${CURRENT}/data/staitc-screen-640x360-300frames.i420.yuv
data=${CURRENT}/data/staitc-screen-320x180-300frames.i420.yuv

rm VideoEncoderTest -rf

${PREFIX}/video_encode_accelerator_tests \
  --codec=vp9 \
  --bitrate=288000\
  --output_bitstream ${data} \
  --gtest_filter=VideoEncoderTest.FlushAtEndOfStream \
  --vmodule=*/media/gpu/*=4 |& tee vea_tests.log
