#!/bin/bash

file=$"/etc/loglocation.sh"
dir=$(dirname "$0")
if [ -e $file ]; then
    echo "export SPATIAL_DATA_ETL_HOME=${dir}" >> $file
elses
    echo "export SPATIAL_DATA_ETL_HOME=${dir}" | sudo tee -a $file
fi
cd src
sudo chmod +x init.sh
sudo chmod +x delt.sh
sudo chmod +x newFile.sh
./init.sh