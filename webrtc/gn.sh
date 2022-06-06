#!/bin/bash -ex

release_build=false

release_flags=""
logging_flags=""
gn_dir="tout/Default"

if [[ $1 == "-r" ]]; then
	release_build=true
fi
echo "Is Release Build: ${release_build}"

if [ ${release_build} == "true" ]; then
	gn_dir="tout/Release"

	release_flags=""
fi

logging_flags="\
    rtc_disable_logging=false \
    rtc_dlog_always_on=true \
    rtc_enable_bwe_test_logging=true \
    enable_log_error_not_reached=true \
    "
gn gen ${gn_dir} \
	--args=" \
    is_debug=false \
    rtc_include_tests=true \
\
    rtc_use_h264 = true \
    proprietary_codecs=true \
    ffmpeg_branding=\"Chrome\" \
\
    ${logging_flags} \
    ${release_flags} \
    "
