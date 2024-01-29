#!/bin/bash -ex

OUT=out_amd64-generic/Release
IP_ADDR=10.239.158.159

deploy_chrome --build-dir=${OUT} --device=$IP_ADDR --force
