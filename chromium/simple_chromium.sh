#!/bin/bash -ex

cros chrome-sdk --board=amd64-generic --nogoma --log-level=debug \
--gn-extra-args=" \
symbol_level=0 \
is_official_build = true \
is_debug=false \
\
rtc_use_h264 = true \
ffmpeg_branding=\"Chrome\" \
proprietary_codecs = true \
\
enable_hangout_services_extension=true \
"