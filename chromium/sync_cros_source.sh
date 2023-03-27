#!/bin/bash
# make the R46 branch repo for BSW
 
# Links for directions and branch names:
# https://wiki.ith.intel.com/display/ChromeOS/Analyzing+Older+OS+Sources+-+Rolling+Back
# http://www.chromium.org/chromium-os/how-tos-and-troubleshooting/working-on-a-branch
# https://chromium.googlesource.com/chromiumos/manifest/+refs
 
REPOS=./          # change this to your path
BRANCH=release-R111-15329.B
 
cd $REPOS
mkdir $BRANCH
cd $BRANCH
 
repo --trace init -b $BRANCH -u https://chromium.googlesource.com/chromiumos/manifest.git --repo-url https://chromium.googlesource.com/external/repo.git
repo sync -j 2
