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
aflwDir="$(pwd)/airflow"
cd data
dataDir=$(pwd)
cd $baseDir
sudo apt-get -y --allow-change-held-packages --allow-remove-essential update
sudo apt install -y wget
sudo apt -y --allow-change-held-packages --allow-remove-essential install postgis postgresql-14-postgis-3
sudo apt -y --allow-change-held-packages --allow-remove-essential install osm2pgsql
sudo apt-get -y install osmosis
sudo apt -y install software-properties-common
sudo add-apt-repository -ppa:deadsnakes/ppa -y
sudo apt -y --allow-change-held-packages --allow-remove-essential install python3
sudo apt -y --allow-change-held-packages --allow-remove-essential install python3-pip
fPath=$(sudo find /etc/postgresql -name 'pg_hba.conf')
sudo sed -i -e 's/md5/trust/g' $fPath
sudo sed -i -e 's/peer/trust/g' $fPath
sudo service postgresql restart
sleep 15s
sudo -u postgres psql -c "create database $DB_NAME;"
sudo -u postgres psql -d $DB_NAME -c "CREATE EXTENSION postgis;"
sudo -u postgres psql -d $DB_NAME -c "CREATE EXTENSION hstore;"
source "ghsl.sh"
while IFS= read -r line || [[ -n "$line" ]]; do
    OIFS=$IFS
    line=$(echo "$line" | sed 's/\r$//')
    if [[ -z "$line" ]]; then
        break
    fi
    stateUrl=$(echo $line | sed "s/-[a-zA-Z0-9_]*.osm.pbf/-updates\/state.txt/")  
    source "${baseDir}/nameParse.sh"
    nameState="${name}_state.txt"
    cd $deltDir
    sudo wget -O $nameState $stateUrl
    nameFile=$"${name}.osm.pbf"
    cd $dataDir
    sudo wget -O $nameFile $line
    osm2pgsql -U $DB_USER -p $name -l -d $DB_NAME $nameFile
    IFS=$OIFS
done < ../src/links.config
export AIRFLOW_HOME=~/airflow
cd ~
mkdir -p airflow/dags
AIRFLOW_VERSION=$"2.9.1"
PYTHON_VERSION="$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
sudo pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
cd $baseDir
mv airflow.py ~/airflow/dags/
airflow standalone