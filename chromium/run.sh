#!/bin/bash -ex

PREFIX=./src/out/Default

use_wayland=false
use_fake_capture=false
use_system_media_driver=false
debug=false

y4m_file=/home/webrtc/Downloads/chromium_video/bbb_1280x720-100frames.y4m

gdb_cmd=""
extra_options=""

#if [ ${use_system_media_driver} == "false" ]; then
  #media_driver_prefix=~/third_party/media_samples/deps/out
#  media_driver_prefix=/opt/jdai12/dev/media_samples/deps/out
#  export LD_LIBRARY_PATH="${media_driver_prefix}/lib"
#  export LIBVA_DRIVERS_PATH="${media_driver_prefix}"
#fi

vainfo

if [ ${use_fake_capture} == "true" ]; then
  extra_options="${extra_options} \
--use-fake-ui-for-media-stream \
--use-fake-device-for-media-stream \
--use-file-for-fake-video-capture=${y4m_file}"
fi

if [ ${use_wayland} == "true" ]; then
  extra_options="${extra_options} \
--ozone-platform=wayland"
fi

if [ ${debug} == "true" ]; then
  gdb_cmd="gdb -args"
  extra_options="${extra_options} \
--debug --single-process"
fi

${gdb_cmd} \
  ${PREFIX}/chrome \
  --use-gl=egl \
  --enable-features=VaapiVideoDecoder,VaapiVideoEncoder \
  --disable-features=UseChromeOSDirectVideoDecoder \
  --ignore-gpu-blocklist \
  --disable-gpu-driver-bug-workaround \
  --vmodule=*/ozone/*=1,*/wayland/*=1,*/vaapi/*=4,*/viz/*=1,*/media/gpu/*=1 \
  --enable-logging=stderr --v=0 \
  ${extra_options} |& tee ./out.log
