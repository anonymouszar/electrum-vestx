#!/bin/bash
set -ev

if [[ -z $TRAVIS_TAG ]]; then
  echo TRAVIS_TAG unset, exiting
  exit 1
fi

BUILD_REPO_URL=https://github.com/anonymouszar/electrum-vestx.git

cd build

git clone --branch $TRAVIS_TAG $BUILD_REPO_URL electrum-vestx

cd electrum-vestx

export PY36BINDIR=/Library/Frameworks/Python.framework/Versions/3.6/bin/
export PATH=$PATH:$PY36BINDIR
source ./contrib/vestx/travis/electrum_vestx_version_env.sh;
echo osx build version is $VESTX_ELECTRUM_VERSION


git submodule init
git submodule update

info "Building CalinsQRReader..."
d=contrib/CalinsQRReader
pushd $d
rm -fr build
xcodebuild || fail "Could not build CalinsQRReader"
popd

sudo pip3 install -r contrib/deterministic-build/requirements.txt
sudo pip3 install -r contrib/deterministic-build/requirements-hw.txt
sudo pip3 install -r contrib/deterministic-build/requirements-binaries.txt
git clone https://github.com/anonymouszar/x16rt_hash x16rt_hash
cd x16rt_hash
sudo python setup.py install
cd ..
sudo pip3 install PyInstaller==3.4 --no-use-pep517

export PATH="/usr/local/opt/gettext/bin:$PATH"
./contrib/make_locale
find . -name '*.po' -delete
find . -name '*.pot' -delete

cp contrib/vestx/osx.spec .
cp contrib/vestx/pyi_runtimehook.py .
cp contrib/vestx/pyi_tctl_runtimehook.py .

pyinstaller \
    -y \
    --name electrum-vestx-$VESTX_ELECTRUM_VERSION.bin \
    osx.spec

info "Adding Vestx URI types to Info.plist"
plutil -insert 'CFBundleURLTypes' \
   -xml '<array><dict> <key>CFBundleURLName</key> <string>dash</string> <key>CFBundleURLSchemes</key> <array><string>vestx</string></array> </dict></array>' \
   -- dist/Vestx\ Electrum.app/Contents/Info.plist \
   || fail "Could not add keys to Info.plist. Make sure the program 'plutil' exists and is installed."

sudo hdiutil create -fs HFS+ -volname "Vestx Electrum" \
    -srcfolder dist/Vestx\ Electrum.app \
    dist/Vestx-Electrum-$VESTX_ELECTRUM_VERSION-macosx.dmg
