#!/bin/bash
##!/bin/bash -ex

## define

URL=$1
#URL=file://~/Videos/BBB_720p_4Mbps_audio_44100_30fps_HP.mp4

Y4M_FILE=~/Videos/bbb_1280x720-100frames.y4m

PREFIX=./src/out/Default

GDB_CMD=""

EXTRA_OPTIONS=""

LOG=out.log

## switch
USE_WAYLAND=true
USE_FAKE_CAPTURE=false
USE_HW_OVERLAY=false
USE_ChromeOSDirectVideoDecoder=true

USE_GDB=false

## switch body
if [ ${USE_FAKE_CAPTURE} == "true" ]; then
  EXTRA_OPTIONS="${EXTRA_OPTIONS} \
--use-fake-device-for-media-stream \
--use-file-for-fake-video-capture=${Y4M_FILE}"
fi

if [ ${USE_GDB} == "true" ]; then
  GDB_CMD="gdb -args"
  EXTRA_OPTIONS="${EXTRA_OPTIONS} \
--debug --single-process"
fi

if [ ${USE_ChromeOSDirectVideoDecoder} == "true" ]; then
  EXTRA_OPTIONS="${EXTRA_OPTIONS} \
--enable-features=VaapiVideoDecoder,VaapiVideoEncoder,UseChromeOSDirectVideoDecoder"
else
  EXTRA_OPTIONS="${EXTRA_OPTIONS} \
--enable-features=VaapiVideoDecoder,VaapiVideoEncoder \
--disable-features=UseChromeOSDirectVideoDecoder"
fi

if [ ${USE_HW_OVERLAY} == "true" ]; then
  EXTRA_OPTIONS="${EXTRA_OPTIONS}"
#--enable-hardware-overlays="single-fullscreen,single-on-top,underlay"
else
  EXTRA_OPTIONS="${EXTRA_OPTIONS} \
--enable-hardware-overlays=\"\""
fi

if [ ${USE_WAYLAND} == "true" ]; then
  EXTRA_OPTIONS="${EXTRA_OPTIONS} \
--ozone-platform=wayland"
else
  EXTRA_OPTIONS="${EXTRA_OPTIONS} \
--ozone-platform=x11"
fi

## run
CMD="\
${gdb_cmd} \
${PREFIX}/chrome \
--use-gl=egl \
--ignore-gpu-blocklist \
--disable-gpu-driver-bug-workaround \
--use-fake-ui-for-media-stream \
--vmodule=*/ozone/*=1,*/wayland/*=1,*/vaapi/*=1,*/viz/*=1,*/media/*=1,*/shared_image/*=1 \
--enable-logging=stderr --v=0 \
${EXTRA_OPTIONS} ${URL}"

echo "" > ${LOG}

echo ${CMD} >> ${LOG}

echo "" >> ${LOG}
vainfo >> ${LOG}

echo "" >> ${LOG}
echo "Start Chromium..." >> ${LOG}
echo "" >> ${LOG}
${CMD} |& tee -a ${LOG}

