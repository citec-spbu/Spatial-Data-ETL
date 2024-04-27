#!/bin/bash

source spatial.config
DB_NAME=$(echo "${DB_NAME,,}")
PGPASSWORD=$DB_PSWD
baseDir=$(pwd)
cd ~
echo $DB_HOST:$DB_PORT:*:$DB_USER:$DB_PSWD%> .pgpass
chmod 600 ~/.pgpass
cd $baseDir
cd ../data
dataDir=$(pwd)
sudo wget -O $PBF_NAME $LINK
cd $baseDir
sudo apt-get -y --allow-change-held-packages --allow-remove-essential update
res=$(pg_config --version)
re='[[:digit:]][[:digit:]]\.*'
sudo apt -y --allow-change-held-packages --allow-remove-essential install postgis postgresql-14-postgis-3
fPath=$(sudo find /etc/postgresql -name 'pg_hba.conf')
sudo sed -i -e 's/md5/trust/g' $fPath
sudo sed -i -e 's/peer/trust/g' $fPath
sudo service postgresql restart
sleep 15s
sudo -u postgres psql -c "create database $DB_NAME;"
sudo -u postgres psql -d $DB_NAME -c "CREATE EXTENSION postgis;"
sudo apt install osm2pgsql
cd $dataDir
osm2pgsql -U $DB_USER -l -d $DB_NAME $PBF_NAME