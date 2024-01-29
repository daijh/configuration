#!/bin/bash -ex

# chrome-linux
GN_DIR_LINUX="out/Release"

# lacros-on_linux
GN_DIR_LACROS="out_linux_lacros/Release"
GN_DIR_ASH="out_linux_ash/Release"

# args
EXTRA_ARGS=""
ARGS="\
chrome_pgo_phase=0 \
symbol_level=1 \
\
is_official_build=false \
dcheck_always_on=false \
is_debug=false \
\
rtc_use_h264=true \
proprietary_codecs=true \
ffmpeg_branding=\"Chrome\" \
\
enable_hangout_services_extension=true \
\
use_system_minigbm=true \
use_intel_minigbm=false \
\
${EXTRA_ARGS}"

# chrome-linux
LINUX_ARGS="\
is_component_build=true \
"
gn gen ${GN_DIR_LINUX} --args="${ARGS} ${LINUX_ARGS}"

# ash
ASH_ARGS="\
target_os=\"chromeos\" \
"
gn gen ${GN_DIR_ASH} --args="${ARGS} ${ASH_ARGS}"

# lacros
LACROS_ARGS="\
target_os=\"chromeos\" \
chromeos_is_browser_only=true \
is_component_build=true \
"
gn gen ${GN_DIR_LACROS} --args="${ARGS} ${LACROS_ARGS}"
