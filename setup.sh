#!/bin/bash

# install dependencies
pip3_path=$(which pip3)
$pip3_path install -r requirements.txt

# find python path
python3_path=$(which python3)

# config path
current_path=$(pwd)
molingo_path=${current_path}/src/molingo.py
sh_path=${current_path}/molingo.sh

echo "${python3_path} ${molingo_path}" > $sh_path
sudo chmod +x $sh_path
bin_file_path=/usr/local/bin/molingo
if [ -f "$bin_file_path" ]; then
    sudo rm $bin_file_path
fi
sudo ln -s $sh_path $bin_file_path
echo "\033[0;32m[Molingo]🎉 Setup Successful, Configure the path in the lingo.yml, and then run \"molingo\" from anywhere\033[0m"