#!/bin/bash
source spatial.config
baseDir=$(pwd)
cd ..
deltDir="$(pwd)/deltas"
dataDir="$(pwd)/data"
line=$1
cd $baseDir
if [ -z $(grep "$line" "links.config") ]; then 
    echo "${line}" >> links.config;
fi
line=$(echo "$line" | sed 's/\r$//')
stateUrl=$(echo $line | sed "s/-[a-zA-Z0-9_]*.osm.pbf/-updates\/state.txt/")  
source "${baseDir}/nameParse.sh"
nameState="${name}_state.txt"
cd $deltDir
sudo wget -O $nameState $stateUrl
nameFile=$"${name}.osm.pbf"
cd $dataDir
sudo wget -O $nameFile $line
osm2pgsql -U $DB_USER -p $name -l -d $DB_NAME $nameFile