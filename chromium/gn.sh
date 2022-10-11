#!/bin/bash -ex

# define
GN_DIR="out/Default"
EXTRA_OPTIONS=""

# switch
USE_SYSTEM_MINIGBM=false
USE_DCHECK=true

# switch body
if [ ${USE_SYSTEM_MINIGBM} == "true" ]; then
  EXTRA_OPTIONS="${EXTRA_OPTIONS} \
use_system_minigbm=true \
use_intel_minigbm=false"
else
  EXTRA_OPTIONS="${EXTRA_OPTIONS} \
use_system_minigbm=false \
use_intel_minigbm=true"
fi

if [ ${USE_DCHECK} == "true" ]; then
  EXTRA_OPTIONS="${EXTRA_OPTIONS} \
dcheck_always_on=true"
else
  EXTRA_OPTIONS="${EXTRA_OPTIONS} \
dcheck_always_on=false"
fi

# run cmd
gn gen ${GN_DIR} \
--args=" \
chrome_pgo_phase=0 \
symbol_level=1 \
is_official_build=true \
is_debug=false \
\
rtc_use_h264=true \
proprietary_codecs=true \
ffmpeg_branding=\"Chrome\" \
\
enable_hangout_services_extension=true \
\
${EXTRA_OPTIONS} "

