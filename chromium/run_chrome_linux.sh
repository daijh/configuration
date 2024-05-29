#!/bin/bash
##!/bin/bash -ex

## using google-chrome
USING_GOOGLE_CHROME=false

## define
URL=$1
Y4M_FILE="~/Videos/bbb_1280x720-100frames.y4m"

PREFIX="src/out/Default"
LOG="chrome_linux.log"

#OZONE_PLATFORM="x11"
OZONE_PLATFORM="wayland"

EXTRA_OPTIONS=""
GDB_CMD=""

## switch
USE_FAKE_CAPTURE=false
USE_GDB=false

#--enable-hardware-overlays="single-fullscreen,single-on-top,underlay"

## switch body
if [ ${USE_FAKE_CAPTURE} == "true" ]; then
  EXTRA_OPTIONS="${EXTRA_OPTIONS} \
--use-fake-device-for-media-stream \
--use-file-for-fake-video-capture=${Y4M_FILE}"
fi

## gdb
if [ ${USE_GDB} == "true" ]; then
  GDB_CMD="gdb -args"
  EXTRA_OPTIONS="${EXTRA_OPTIONS} \
--debug --single-process"
fi

CHROME_EXE="${PREFIX}/chrome"
if [ ${USING_GOOGLE_CHROME} == "true" ]; then
    CHROME_EXE="google-chrome"
fi

# mesa dump
export MESA_GLSL=source,log,useprog
export MESA_SHADER_DUMP_PATH=/tmp/MESA_SHADER_DUMP_PATH
export MESA_SHADER_CAPTURE_PATH=/tmp/MESA_SHADER_CAPTURE_PATH

mkdir -p ${MESA_SHADER_DUMP_PATH}
mkdir -p ${MESA_SHADER_CAPTURE_PATH}

mkdir -p /tmp/angle_shaders
export ANGLE_SHADER_DUMP_PATH=/tmp/angle_shaders

## run
CMD="\
${GDB_CMD} \
${CHROME_EXE} \
--ignore-gpu-blocklist \
--disable-gpu-driver-bug-workaround \
\
--use-fake-ui-for-media-stream \
\
--enable-features=VaapiVideoDecodeLinuxGL,VaapiVideoDecoder,VaapiVideoEncoder,UseChromeOSDirectVideoDecoder \
\
--use-gl=angle --use-angle=gl \
\
--ozone-platform=${OZONE_PLATFORM} \
\
--vmodule=*/ozone/*=1,*/wayland/*=1,*/vaapi/*=1,*/viz/*=1,*/media/*=1,*/shared_image/*=1 \
--enable-logging=stderr --v=0 \
\
--disable-gpu-sandbox \
--enable-angle-features=dumpShaderSource \
--enable-angle-features=enableShaderSubstitution \
--enable-angle-features=dumpShaderSource,enableShaderSubstitution \
\
${EXTRA_OPTIONS} \
${URL}"

# Start
echo -e ${CMD}"\n" > ${LOG}
vainfo >> ${LOG}
echo -e "\nStart Chromium...\n" >> ${LOG}
${CMD} |& tee -a ${LOG}
