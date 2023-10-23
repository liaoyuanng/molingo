
#!/bin/bash
pip3_path=$(which pip3)
$pip3_path install -r requirements.txt

> molingo.sh

python3_path=$(which python3)

current_path=$(pwd)
molingo_path=${current_path}/src/molingo.py
sh_path=${current_path}/molingo.sh

echo "${python3_path} ${molingo_path}" > $sh_path
sudo chmod +x $sh_path
sudo rm /usr/local/bin/molingo
sudo ln -s $sh_path /usr/local/bin/molingo
