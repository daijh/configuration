#!/bin/bash -ex

SDK_BOARD=amd64-generic
IP_ADDR=172.25.235.137

deploy_chrome --build-dir=out_${SDK_BOARD}/Release --device=$IP_ADDR
