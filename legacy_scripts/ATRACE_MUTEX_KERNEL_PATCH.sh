#!/bin/sh

#build file list
files=`grep "mutex_[lu].*(mode_config|struct_mutex)" *.c i915/*.c -Es | awk -F: '{print $1}' | sort -u`

#handle special, mutex_lock_interruptible
sed 's/\(.*\)mutex_lock_interruptible(\(.*struct_mutex.*\))/\1ATRACE_MUTEX_LOCK_INTERRUPTIBLE(\2, 1)/g' i915/i915_gem.c -i

for file in $files
do
    #Patch mode_config, stuct_mutex  
    sed 's/\(.*\)mutex_lock(\(.*mode_config.*mutex.*\))/\1ATRACE_MUTEX_LOCK(\2, 0)/g' $file -i
    sed 's/\(.*\)mutex_unlock(\(.*mode_config.*mutex.*\))/\1ATRACE_MUTEX_UNLOCK(\2, 0)/g' $file -i
    sed 's/\(.*\)mutex_lock_interruptible(\(.*mode_config.*mutex.*\))/\1ATRACE_MUTEX_LOCK_INTERRUPTIBLE(\2, 0)/g' $file -i

    sed 's/\(.*\)mutex_lock(\(.*mode_config.*fb_lock.*\))/\1ATRACE_MUTEX_LOCK(\2, 0)/g' $file -i
    sed 's/\(.*\)mutex_unlock(\(.*mode_config.*fb_lock.*\))/\1ATRACE_MUTEX_UNLOCK(\2, 0)/g' $file -i

    sed 's/\(.*\)mutex_lock(\(.*struct_mutex.*\))/\1ATRACE_MUTEX_LOCK(\2, 0)/g' $file -i
    sed 's/\(.*\)mutex_unlock(\(.*struct_mutex.*\))/\1ATRACE_MUTEX_UNLOCK(\2, 0)/g' $file -i
    sed 's/\(.*\)mutex_lock_interruptible(\(.*struct_mutex.*\))/\1ATRACE_MUTEX_LOCK_INTERRUPTIBLE(\2, 0)/g' $file -i

    #Patch include  
    if test -z "`grep "drm_trace.h" -o $file`"
    then
        line=`grep "#include.*(drm|i915)" -Enh $file | tail -n 1 | awk -F: '{print $1}'`
        sed "${line},${line} a\#include \"drm_trace.h\"" $file -i
    fi
done

#Patch Makefile
if test -z "`grep \"\-Idrivers/gpu/drm\" -o i915/Makefile`"
then
    sed 's/\(^ccflags.*\)/\1 -Idrivers\/gpu\/drm/g' i915/Makefile -i
fi

#verify
#grep "mutex_[lu].*(mode_config|struct_mutex)" *.c i915/*.c -Ens

#done 
echo "Apply patch done!"
