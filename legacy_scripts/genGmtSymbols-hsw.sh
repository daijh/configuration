#!/bin/sh

if [ $# -ne 1 ] # while there are still arguments
then
    echo "Error: Require symbols library path" 
    return 
fi

libs="
    libdrm.so 
    libdrm_intel.so
    i965_drv_video.so
    libmfxhw32.so
    libmfx_omx_components_hw.so
    libmfx_omx_core.so
    libva-android.so
    libva.so
    libva-tpi.so
    "
hwlibs="
    camera.bigcore.so
    gralloc.bigcore.so
    "
libs_path=$1/system/lib
hw_libs_path=$1/system/lib/hw

#echo $libs_path
#echo $hw_libs_path

for name in $libs
do
    if test -e $libs_path/$name
    then
        nm -C --defined-only -v -e $libs_path/$name > $name.symbols
    else
        echo "$libs_path/$name does not exist!"
    fi 
done

for name in $hwlibs
do
    if test -e $hw_libs_path/$name
    then
        nm -C --defined-only -v -e $hw_libs_path/$name > $name.symbols
    else
        echo "$hw_libs_path/name does not exist!"
    fi 
done

