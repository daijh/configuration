#!/bin/bash -ex

#OUT=out_amd64-generic/Release
OUT=out_amd64-generic/base-build
#OUT=out_amd64-generic/opt-event-log+p2p-build
IP_ADDR=10.239.158.125

deploy_chrome --build-dir=${OUT} --device=$IP_ADDR
