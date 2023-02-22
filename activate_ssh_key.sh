#!/bin/bash

if [ $# -ne 1 ]; then
  echo "Usage: $0 ssh_key"
  exit
fi

SSH_KEY=$1
echo "Add ssh_key: ${SSH_KEY}"

eval `ssh-agent -s`
ssh-add ${SSH_KEY}

