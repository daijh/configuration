#!/bin/sh

if [ $# -ne 1 ]
then
    echo "Error: Require USB device name!"
    return
fi

if [ ! -f ./out/target/product/core_ufo/live.img ] #-s file exists and has a size greater than zero. 
then
    echo "Error: ./out/target/product/core_ufo/live.img does not exist!"
    return
fi

if [ ! -b $1 ] #-s file exists and has a size greater than zero. 
then
    echo "Error: $1 is not a block device!"
    return
fi

echo "Begin burn USB deivce..."

sudo dd if=./out/target/product/core_ufo/live.img of=$1 bs=1M;
sync;
