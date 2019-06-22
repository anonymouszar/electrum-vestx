#!/bin/bash

source ./contrib/vestxl/travis/electrum_vestx_version_env.sh;
echo wine build version is $VESTX_ELECTRUM_VERSION

mv /opt/zbarw $WINEPREFIX/drive_c/

mv /opt/x16rt_hash $WINEPREFIX/drive_c/

mv /opt/libsecp256k1/libsecp256k1-0.dll \
   /opt/libsecp256k1/libsecp256k1.dll
mv /opt/libsecp256k1 $WINEPREFIX/drive_c/

cd $WINEPREFIX/drive_c/electrum-vestx

rm -rf build
rm -rf dist/electrum-vestx

cp contrib/vestx/deterministic.spec .
cp contrib/vestx/pyi_runtimehook.py .
cp contrib/vestx/pyi_tctl_runtimehook.py .

wine python -m pip install -r contrib/deterministic-build/requirements.txt
wine python -m pip install -r contrib/deterministic-build/requirements-hw.txt
wine python -m pip install -r contrib/deterministic-build/requirements-binaries.txt
wine python -m pip install PyInstaller==3.4 --no-use-pep517

wine pyinstaller -y \
    --name electrum-vestx-$VESTX_ELECTRUM_VERSION.exe \
    deterministic.spec

if [[ $WINEARCH == win32 ]]; then
    NSIS_EXE="$WINEPREFIX/drive_c/Program Files/NSIS/makensis.exe"
else
    NSIS_EXE="$WINEPREFIX/drive_c/Program Files (x86)/NSIS/makensis.exe"
fi

wine "$NSIS_EXE" /NOCD -V3 \
    /DPRODUCT_VERSION=$VESTX_ELECTRUM_VERSION \
    /DWINEARCH=$WINEARCH \
    contrib/vestx/electrum-vestx.nsi
