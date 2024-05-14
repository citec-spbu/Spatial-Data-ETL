#!/bin/bash

source spatial.config
DB_NAME=$(echo "${DB_NAME,,}")
PGPASSWORD=$DB_PSWD
baseDir=$(pwd)
cd ~
echo $DB_HOST:$DB_PORT:*:$DB_USER:$DB_PSWD%> .pgpass
chmod 600 ~/.pgpass
cd $baseDir
cd ..
deltDir="$(pwd)/deltas"
cd data
dataDir=$(pwd)
cd $baseDir
sudo apt-get -y --allow-change-held-packages --allow-remove-essential update
sudo apt -y --allow-change-held-packages --allow-remove-essential install postgis postgresql-14-postgis-3
sudo apt -y --allow-change-held-packages --allow-remove-essential install osm2pgsql
sudo apt-get -y install osmosis
fPath=$(sudo find /etc/postgresql -name 'pg_hba.conf')
sudo sed -i -e 's/md5/trust/g' $fPath
sudo sed -i -e 's/peer/trust/g' $fPath
sudo service postgresql restart
sleep 15s
sudo -u postgres psql -c "create database $DB_NAME;"
sudo -u postgres psql -d $DB_NAME -c "CREATE EXTENSION postgis;"
sudo -u postgres psql -d $DB_NAME -c "CREATE EXTENSION hstore;"
cd $deltDir
#У регионов одинаковый state.txt, поэтому можно любой поставить
sudo wget -O state.txt https://download.geofabrik.de/russia/central-fed-district-updates/state.txt
cd $dataDir
while IFS= read -r line || [[ -n "$line" ]]; do
    if [[ -z "$line" ]]; then
        break
    fi
    line=$(echo "$line" | sed 's/\r$//')
    wordsArr=$(echo ${line} | awk -F'/' '{print $5}')
    words=$(echo $wordsArr | tr "-" "\n")
    name=""
    for word in $words;
    do
        if [[ $word == "fed" ]]; then
            break
        fi
        name="${name}${word}-"
    done
    name=${name%?}
    nameFile=$"$name.osm.pbf"
    sudo wget -O $nameFile $line
    osm2pgsql -U $DB_USER -p $name -l -d $DB_NAME $nameFile
done < ../src/links.config