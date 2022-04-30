#!/bin/bash -ex

OUTPUT=gcc.log

./src/out/Default/peerconnection_unittests |&
	tee $OUTPUT

echo "===Done==="
grep -E "PASSED|FAILED" $OUTPUT
