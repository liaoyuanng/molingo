bin_file_path=/usr/local/bin/molingo
if [ -f "$bin_file_path" ]; then
    sudo rm $bin_file_path
fi