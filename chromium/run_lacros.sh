#!/bin/bash
##!/bin/bash -ex

## define
URL=$1
Y4M_FILE="~/Videos/bbb_1280x720-100frames.y4m"

PREFIX_LACROS="src/out_linux_lacros/Release"
PREFIX_ASH="src/out_linux_ash/Release"

LOG="lacros.log"
EXTRA_OPTIONS=""

## switch
USE_FAKE_CAPTURE=false

#--enable-hardware-overlays="single-fullscreen,single-on-top,underlay"

## switch body
if [ ${USE_FAKE_CAPTURE} == "true" ]; then
  EXTRA_OPTIONS="${EXTRA_OPTIONS} \
--use-fake-device-for-media-stream \
--use-file-for-fake-video-capture=${Y4M_FILE}"
fi

## run
mkdir -p /tmp/ash_chrome_xdg_runtime
rm -rf /tmp/ash-chrome

CMD="\
${PREFIX_ASH}/chrome \
--user-data-dir=/tmp/ash-chrome \
--enable-wayland-server \
--no-startup-window \
--login-manager --login-profile=user \
--enable-features=LacrosOnly \
--lacros-chrome-path=${PREFIX_LACROS}/chrome \
--lacros-chrome-additional-args=--gpu-sandbox-start-early \
${EXTRA_OPTIONS} \
${URL}"

# Start
echo -e ${CMD}"\n" > ${LOG}
vainfo >> ${LOG}
echo -e "\nStart Chromium...\n" >> ${LOG}

export XDG_RUNTIME_DIR=/tmp/ash_chrome_xdg_runtime
${CMD} |& tee -a ${LOG}
