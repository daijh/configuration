#!/bin/bash -ex

release_build=false

release_flags=""
gn_dir="out/Default"

if [[ $1 == "-r" ]]; then
	release_build=true
fi
echo "Is Release Build: ${release_build}"

if [ ${release_build} == "true" ]; then
    gn_dir="out/Release"

	release_flags=" \
        symbol_level=0 \
        "
fi

gn gen ${gn_dir} \
	--args=" \
    is_official_build=false \
    is_debug=false \
\
    rtc_use_h264 = true \
    proprietary_codecs=true \
    ffmpeg_branding=\"Chrome\" \
\
    enable_hangout_services_extension=true \
    ${release_flags} \
    "
