#!/bin/bash -ex

#volteer usb camera
IP=10.239.158.147

function MakeSVCTestCast() {
    lock=$1

    echo webrtc.RTCPeerConnectionPerf.vp9_hw_svc_l3t3_key${va_lock}
}

function MakeVideoLayoutTestCast() {
    layout=$1
    lock=$2

    echo webrtc.RTCPeerConnectionPerf.vp9_hw_multi_vp9_${layout}${va_lock}
}

function RunRTCPeerConnectionPerf() {
    loop=$1
    case=$2

    echo "case:", ${case}

    i=0
    while [ $i -lt ${loop} ]; do
        tast -verbose run root@${IP} ${case}
        sleep 300
        ((i++))
    done
}

RunRTCPeerConnectionPerf 6 `MakeSVCTestCast "_global_vaapi_lock_disabled"`
RunRTCPeerConnectionPerf 6 `MakeSVCTestCast ""`

RunRTCPeerConnectionPerf 6 `MakeVideoLayoutTestCast "3x3"  "_global_vaapi_lock_disabled"`
RunRTCPeerConnectionPerf 6 `MakeVideoLayoutTestCast "3x3"  ""`

RunRTCPeerConnectionPerf 6 `MakeVideoLayoutTestCast "4x4"  "_global_vaapi_lock_disabled"`
RunRTCPeerConnectionPerf 6 `MakeVideoLayoutTestCast "4x4"  ""`

