#!/bin/bash -ex

logging_flags=""
gn_dir="out/Default"

logging_flags="\
#    rtc_disable_logging=false \
#    rtc_dlog_always_on=true \
#    rtc_enable_bwe_test_logging=true \
#    enable_log_error_not_reached=true \
    "
gn gen ${gn_dir} \
  --args=" \
    is_debug=true \
    rtc_include_tests=true \
\
    rtc_use_h264 = true \
    proprietary_codecs=true \
    ffmpeg_branding=\"Chrome\" \
\
    "
