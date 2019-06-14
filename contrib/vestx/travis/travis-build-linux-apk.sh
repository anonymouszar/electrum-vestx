#!/bin/bash
set -ev

if [[ -z $TRAVIS_TAG ]]; then
  echo TRAVIS_TAG unset, exiting
  exit 1
fi

BUILD_REPO_URL=https://github.com/akhavr/electrum-vestx.git

cd build

git clone --branch $TRAVIS_TAG $BUILD_REPO_URL electrum-vestx

pushd electrum-vestx
./contrib/make_locale
find . -name '*.po' -delete
find . -name '*.pot' -delete
popd

sudo chown -R 1000 electrum-vestx

docker run --rm \
    -v $(pwd)/electrum-vestx:/home/buildozer/build \
    -t zebralucky/electrum-vestx-winebuild:Kivy33x bash -c \
    'rm -rf packages && ./contrib/make_packages && ./contrib/make_apk'
