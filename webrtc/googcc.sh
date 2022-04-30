#!/bin/bash -ex

OUTPUT=gcc.log

./src/out/Default/modules_unittests --gtest_filter="*GoogCc*" |&
	tee $OUTPUT

echo "===Done==="
grep -E "PASSED|FAILED" $OUTPUT
