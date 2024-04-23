#!/bin/bash

#. spatial.config
while IFS="\r" read -r line;
do
        line=${line%?}
        eval "$line";
done < spatial.config
DB_NAME=$(echo "${DB_NAME,,}")
PGPASSWORD=$DB_PSWD
baseDir=$(pwd)
cd ~
echo "localhost:5432:$DB_NAME:$DB_USER:$DB_PSWD" >> .pgpass
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
sudo sed -i -e 's/md5/peer/g' $fPath
sudo service postgresql restart
sleep 15s
sudo apt install postgis postgresql-$psqlVer-postgis-3
sudo -u postgres psql -c "create database $DB_NAME;"
sudo -u postgres psql -d $DB_NAME -c "CREATE EXTENSION postgis;"
sudo sed -i -e 's/peer/md5/g' $fPath
sudo service postgresql restart
sudo apt install osm2pgsql
osm2pgsql -U $DB_USER -l -W -d $DB_NAME -H localhost $pbfName