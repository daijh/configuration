#Author: jabin

if [ $# = 1 ]; then
	echo $1 > /sys/devices/pci0000:00/0000:00:02.0/drm/card0/gt_max_freq_mhz
	echo $1 > /sys/devices/pci0000:00/0000:00:02.0/drm/card0/gt_min_freq_mhz
	sleep 1
fi
echo -n "Current GPU frequency:"
cat /sys/devices/pci0000:00/0000:00:02.0/drm/card0/gt_cur_freq_mhz
