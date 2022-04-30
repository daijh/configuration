KERNEL_PATH='/opt/WorkDir/android/l-android/kernel/gmin'
SOCWATCH_PATH='/opt/WorkDir/android/l-android/socwatch/socwatch_android_INTERNAL'

PERF_DRIVER_PATH=$SOCWATCH_PATH/soc_perf_driver
SOCWATCH_DRIVER_PATH=$SOCWATCH_PATH/socwatch_driver/lx_kernel

# build perf driver
make clean -C $KERNEL_PATH M=$PERF_DRIVER_PATH/src PWD=$PERF_DRIVER_PATH/src
make modules -C $KERNEL_PATH M=$PERF_DRIVER_PATH/src  PWD=$PERF_DRIVER_PATH/src LDDINCDIR=$PERF_DRIVER_PATH/src/../include LDDINCDIR1=$PERF_DRIVER_PATH/src/inc

# build socwatch driver
make clean -C $KERNEL_PATH M=$SOCWATCH_DRIVER_PATH PWD=$SOCWATCH_DRIVER_PATH
make modules -C $KERNEL_PATH M=$SOCWATCH_DRIVER_PATH PWD=$SOCWATCH_DRIVER_PATH

# sign
for name in `find $SOCWATCH_PATH -name "*ko"` 
do
	driver_basename=`basename $name`

	if test -e $driver_basename
	then
		rm -v $driver_basename
	fi	

	echo "sing $name -> $driver_basename"
	perl sign-file sha256  ${KERNEL_PATH}/signing_key.priv ${KERNEL_PATH}/signing_key.x509 $name $driver_basename
done

