#!/bin/bash

rm -rf test_release
mkdir test_release
cp dist/pac_man_linux.zip test_release/

cd test_release || exit 1
unzip pac_man_linux.zip

cd pac_man || exit 1
./pac_man config.json