#!/bin/bash -ex

OUT=out_amd64-generic/Release
#OUT=out_amd64-generic/default-build
IP_ADDR=10.239.158.73

deploy_chrome --build-dir=${OUT} --device=$IP_ADDR
