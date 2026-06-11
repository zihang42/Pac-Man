#!/bin/bash
rm -rf test_release
mkdir test_release
cp dist/pac_man_linux.zip test_release/
cd test_release
unzip pac_man_linux.zip
cd dist/pac_man
./pac_man