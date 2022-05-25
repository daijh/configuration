#!/bin/bash -ex

THIS=$(realpath $0)
if [ ! -f ${THIS} ]; then
  THIS=$0
fi

cd && mkdir -p mipi && cd mipi
TOPDIR=$(pwd)

#install the required packages
Setup() {
  sudo apt-get install -y git libexpat-dev automake libtool libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev build-essential cmake libpciaccess-dev valgrind v4l-utils libopts25 autogen libffi-dev
}

#Syncing the source code
Sync_Source_Code() {
  cd ${TOPDIR}
  rm -rf ipu6-drivers ipu6-camera-bins/ ipu6-camera-hal/ icamerasrc/ v4l2loopback/
  git clone https://github.com/intel/ipu6-drivers.git -b ccg_plat_adlp --single-branch
  cd ipu6-drivers
  git checkout d74defa4563996b4835a9164076f8b832ca85339
  cd ${TOPDIR}
  git clone https://github.com/intel/ipu6-camera-bins.git -b ccg_plat_adlp --single-branch
  cd ipu6-camera-bins/
  git checkout 0a8fa1c7b910be070e5b939a5bb1a9cd6ec3da90
  cd ${TOPDIR}
  git clone https://github.com/intel/ipu6-camera-hal.git -b ccg_plat_adlp --single-branch
  cd ipu6-camera-hal/
  git checkout 37773d5e68a9295aa96606ce580ed341b657df67
  mkdir -p ./build/out/install/usr
  cd ${TOPDIR}
  git clone https://github.com/intel/icamerasrc.git -b icamerasrc_slim_api --single-branch
  cd icamerasrc/
  git checkout a35978264002acaad72bb9956238ccaef3743932
  sed -i 's/1.10/foreign/' configure.ac
  cd ${TOPDIR}
  git clone https://github.com/umlaeute/v4l2loopback -b v0.12.5 --single-branch
  cd ${TOPDIR}
}

install_IPU6_HAL() {
  cd ${TOPDIR}/ipu6-camera-hal/build
  cmake -DCMAKE_BUILD_TYPE=Release -DIPU_VER=ipu6ep -DPRODUCTION_NAME=ccg_platform -DENABLE_VIRTUAL_IPU_PIPE=OFF -DUSE_PG_LITE_PIPE=ON -DUSE_STATIC_GRAPH=OFF -DCMAKE_INSTALL_PREFIX=/usr ..
  make -j8
  #sudo make install
}

install_icamerasrc_plugin() {
  cd ${TOPDIR}/icamerasrc
  #sudo chmod +x autogen.sh
  ./autogen.sh
  make
  #sudo make install
}

install_v4l2loopback_driver() {
  cd ${TOPDIR}/v4l2loopback
  #make clean && make && sudo make install && sudo depmod -a
}

echo ${TOPDIR}
return

Setup
Sync_Source_Code
#sudo cp -r ${TOPDIR}/ipu6-camera-bins/include/* /usr/include/
#sudo cp -r ${TOPDIR}/ipu6-camera-bins/lib/* /usr/lib/
install_IPU6_HAL
export CHROME_SLIM_CAMHAL=ON
export STRIP_VIRTUAL_CHANNEL_CAMHAL=ON
install_icamerasrc_plugin
install_v4l2loopback_driver
