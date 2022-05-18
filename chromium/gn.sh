#!/bin/bash -ex

release_build=false

release_flags=""
gn_dir="tout/Default"

if [[ $1 == "-r" ]]; then
	release_build=true
fi
echo "Is Release Build: ${release_build}"

if [ ${release_build} == "true" ]; then
    gn_dir="tout/Release"

	release_flags=" \
        is_official_build=true \
        symbol_level=0 \
        disable_fieldtrial_testing_config=true \
        "
fi

gn gen ${gn_dir} \
	--args=" \
    is_debug=false \
    enable_hangout_services_extension=true \
    proprietary_codecs=true \
    ffmpeg_branding=\"Chrome\" \
    ${release_flags}
    "
