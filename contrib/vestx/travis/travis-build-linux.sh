#!/bin/bash
set -ev

if [[ -z $TRAVIS_TAG ]]; then
  echo TRAVIS_TAG unset, exiting
  exit 1
fi

BUILD_REPO_URL=https://github.com/anonymouszar/electrum-vestx.git

cd build

git clone --branch $TRAVIS_TAG $BUILD_REPO_URL electrum-vestx

mkdir -p electrum-vestx/dist
wget -O electrum-vestx/dist/tor-proxy-setup.exe \
    https://github.com/zebra-lucky/tor-proxy/releases/download/0.3.5.8/tor-proxy-0.3.5.8-setup.exe


docker run --rm \
    -v $(pwd):/opt \
    -w /opt/electrum-vestx \
    -t zebralucky/electrum-dash-winebuild:LinuxPy36 /opt/build_linux.sh

sudo find . -name '*.po' -delete
sudo find . -name '*.pot' -delete


docker run --rm \
    -v $(pwd):/opt \
    -w /opt/electrum-vestx/contrib/vestx/travis \
    -t zebralucky/electrum-dash-winebuild:LinuxAppImage ./build_appimage.sh


export WINEARCH=win32
export WINEPREFIX=/root/.wine-32
export PYHOME=$WINEPREFIX/drive_c/Python36

wget https://github.com/zebra-lucky/zbarw/releases/download/20180620/zbarw-zbarcam-0.10-win32.zip
unzip zbarw-zbarcam-0.10-win32.zip && rm zbarw-zbarcam-0.10-win32.zip

wget https://github.com/anonymouszar/x16rt_hash/releases/download/v1.0.0/x16rt_hash-1.0.0-win32.zip
unzip x16rt_hash-1.0.0-win32.zip && rm x16rt_hash-1.0.0-win32.zip

wget https://github.com/zebra-lucky/secp256k1/releases/download/0.1/libsecp256k1-0.1-win32.zip
unzip libsecp256k1-0.1-win32.zip && rm libsecp256k1-0.1-win32.zip

docker run --rm \
    -e WINEARCH=$WINEARCH \
    -e WINEPREFIX=$WINEPREFIX \
    -e PYHOME=$PYHOME \
    -v $(pwd):/opt \
    -v $(pwd)/electrum-vestx/:$WINEPREFIX/drive_c/electrum-vestx \
    -w /opt/electrum-vestx \
    -t zebralucky/electrum-dash-winebuild:WinePy36 /opt/build_wine.sh

export WINEARCH=win64
export WINEPREFIX=/root/.wine-64
export PYHOME=$WINEPREFIX/drive_c/Python36

wget https://github.com/zebra-lucky/zbarw/releases/download/20180620/zbarw-zbarcam-0.10-win64.zip
unzip zbarw-zbarcam-0.10-win64.zip && rm zbarw-zbarcam-0.10-win64.zip

https://github.com/anonymouszar/x16rt_hash/releases/download/v1.0.0/x16rt_hash-1.0.0-win64.zip
unzip x16rt_hash-1.0.0-win64.zip && rm x16rt_hash-1.0.0-win64.zip

wget https://github.com/zebra-lucky/secp256k1/releases/download/0.1/libsecp256k1-0.1-win64.zip
unzip libsecp256k1-0.1-win64.zip && rm libsecp256k1-0.1-win64.zip

docker run --rm \
    -e WINEARCH=$WINEARCH \
    -e WINEPREFIX=$WINEPREFIX \
    -e PYHOME=$PYHOME \
    -v $(pwd):/opt \
    -v $(pwd)/electrum-vestx/:$WINEPREFIX/drive_c/electrum-vestx \
    -w /opt/electrum-vestx \
    -t zebralucky/electrum-dash-winebuild:WinePy36 /opt/build_wine.sh
