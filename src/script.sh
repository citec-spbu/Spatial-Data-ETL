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
sudo apt-get update
if !(which psql>/dev/null)
then sudo apt install postgresql=14.11
fi
res=$(pg_config --version)
re='[[:digit:]][[:digit:]]\.*'
psqlVer=14
for word in $res; do
        if [[ $word =~ [0-9][0-9]\.* ]]; then
                psqlVer=$(echo $word | cut -f1 -d.)
                break
        fi
done

fPath=$(sudo find /etc/postgresql -name 'pg_hba.conf')
sudo sed -i -e 's/md5/trust/g' $fPath
sudo sed -i -e 's/peer/trust/g' $fPath
sudo service postgresql restart
sleep 15s
sudo apt install postgis postgresql-$psqlVer-postgis-3
sudo -u postgres psql -c "create database $DB_NAME;"
sudo -u postgres psql -d $DB_NAME -c "CREATE EXTENSION postgis;"
sudo apt install osm2pgsql
cd $dataDir
osm2pgsql -U $DB_USER -l -d $DB_NAME $PBF_NAME