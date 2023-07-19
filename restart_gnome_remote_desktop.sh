#!/bin/bash

if [ $# -ne 1 ]; then
  echo "Usage: $0 password"
  exit
fi

PASSWORD=$1
echo "Set password: ${PASSWORD}"

killall gnome-keyring-daemon
echo -n ${PASSWORD} | gnome-keyring-daemon -l -d
gnome-keyring-daemon -s
#systemctl --user daemon-reload
systemctl --user restart gnome-remote-desktop
systemctl --user status gnome-remote-desktop
