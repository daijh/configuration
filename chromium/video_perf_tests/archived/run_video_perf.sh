#!/bin/bash

#PREFIX=/PATH_TO_MEDIA_DRIVER
#export LD_LIBRARY_PATH=${PREFIX}/lib
#export LIBVA_DRIVERS_PATH=${PREFIX}/lib

PROGRAM_PATH=./src/out/Default

function RunDecPerfTest() {
	local params=$1
	local loop=1
	local program="${PROGRAM_PATH}/video_decode_accelerator_perf_tests \
--vmodule=*/ozone/*=4,*/wayland/*=4,*/vaapi/*=4,*/media/*=0,*/viz/*=4 \
$params"

	local counter=1
	while [[ $counter -le loop ]]; do
		echo "Loop: $counter"
		$program |& tee ./video_dec_perf-$counter.log

		((counter++))
	done
}

function RunEncPerfTest() {
	local params=$1
	local loop=1
	local program="${PROGRAM_PATH}/video_encode_accelerator_perf_tests \
--vmodule=*/ozone/*=4,*/wayland/*=4,*/vaapi/*=4,*/media/*=0,*/viz/*=4 \
$params"

	local counter=1
	while [[ $counter -le loop ]]; do
		echo "Loop: $counter"
		$program |& tee ./video_enc_perf-$counter.log

		((counter++))
	done
}

program_params=${@}
if [[ $1 == "-d" ]]; then
	RunDecPerfTest "${program_params[@]:2}"
elif [[ $1 == "-e" ]]; then
	RunEncPerfTest "${program_params[@]:2}"
else
	echo "Usage: $0 [-d|-e] video_accelerator_perf_tests_params"
fi
