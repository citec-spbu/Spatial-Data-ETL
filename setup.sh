#!/bin/bash
mkdir data
mkdir deltas
dir=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd src
path="${dir}/src/delt.sh "
sed -i -e "s|PATH_TO_SCRIPT|$path|g" airflow.py
sudo chmod +x init.sh
sudo chmod +x delt.sh
sudo chmod +x newFile.sh
./init.sh