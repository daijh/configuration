#!/bin/bash -ex

PREFIX=./src/out/Default

use_wayland=false
use_fake_capture=false
use_system_media_driver=true
debug=false

y4m_file=/home/webrtc/Downloads/chromium_video/bbb_1280x720-100frames.y4m

gdm_cmd=""
extra_options=""

if [ ${use_fake_capture} == "true" ]; then
  extra_options="${extra_options} \
--use-fake-ui-for-media-stream \
--use-fake-device-for-media-stream \
--use-file-for-fake-video-capture=${y4m_file}"
fi

if [ ${use_wayland} == "true" ]; then
  extra_options="${extra_options} \
--ozone-platform=wayland"
else
  extra_options="${extra_options} \
--ozone-platform=x11"
fi

if [ ${debug} == "true" ]; then
  gdm_cmd="gdb -args --single-process"
  extra_options="${extra_options} \
--debug"
fi

if [ ${use_system_media_driver} == "true" ]; then
  media_driver_prefix=~/third_party/media_samples/deps/out
  export LD_LIBRARY_PATH="${media_driver_prefix}/lib"
  export LIBVA_DRIVERS_PATH="${media_driver_prefix}"
fi

${gdm_cmd} \
  ${PREFIX}/chrome \
  --enable-benchmarking \
  --enable-experimental-web-platform-features \
  --vmodule=*/ozone/*=1,*/wayland/*=1,*/vaapi/*=1,*/viz/*=1,*/media/gpu/*=1 \
  --enable-logging=stderr --v=0 \
  --use-gl=egl \
  --enable-accelerated-video-decoder \
  --enable-features=VaapiVideoDecoder,VaapiVideoEncoder \
  --disable-features=Vulkan,UseChromeOSDirectVideoDecoder \
  --ignore-gpu-blocklist \
  --disable-gpu-driver-bug-workaround \
  --no-sandbox \
  ${extra_options} |&
  tee ./out.log
