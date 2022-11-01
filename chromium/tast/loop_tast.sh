#!/bin/bash

echo "Bash version ${BASH_VERSION}..."

set -o errexit
set -o nounset
set -o pipefail

#volteer usb camera
IP=10.239.158.120

function RunTastCases() {
  loop=$(($1))
  case=$2

  echo "RUN ${case} x${loop}"
  for i in {1..5}; do
    echo "Loop ${i}"
    tast -verbose run root@${IP} ${case}
    sleep 30
  done
}

RunTastCases 6 "webrtc.RTCPeerConnectionPerf.vp9_hw_multi_vp9_3x3"
RunTastCases 6 "webrtc.RTCPeerConnectionPerf.vp9_hw_multi_vp9_3x3_global_vaapi_lock_disabled"
