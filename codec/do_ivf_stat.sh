##!/bin/bash -ex
THIS=$(realpath $(pwd)/$BASH_SOURCE)
if [ ! -f ${THIS} ]; then
  THIS=$(realpath $BASH_SOURCE)
fi
CURRENT=$(dirname ${THIS})

# Support VP9.
if [ $# -ne 1 ]; then
  echo "Usage: $0 vp9.ivf"
  exit
fi

INPUT=$1
OUTPUT=$(basename $1).trace_header
STAT_OUTPUT=${OUTPUT}.stat

rm -v ${OUTPUT} ${STAT_OUTPUT}

ffmpeg -i ${INPUT} -vcodec copy -bsf:v trace_headers -f null - |& tee ${OUTPUT}
ack "(base_q_idx|Packet)" ${OUTPUT} |& tee ${STAT_OUTPUT}
ack "base_q_idx" ${OUTPUT} | wc -l

echo "input: ${INPUT}"
echo "trace_headers: ${OUTPUT}"
echo "stat: ${STAT_OUTPUT}"
