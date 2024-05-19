#!/bin/bash
scriptDir=$(dirname "$0")
cd $scriptDir
source spatial.config
cd ..
baseDir=$(pwd)
deltDir=$"${baseDir}/deltas"
cd $deltDir
sudo chmod a+w .
rm -f configuration.txt
osmosis --read-replication-interval-init workingDirectory=$deltDir
while IFS= read -r line || [[ -n "$line" ]]; do
    line=$(echo "$line" | sed 's/\r$//')
    if [[ -z "$line" ]]; then
        break
    fi
    source "${baseDir}/src/nameParse.sh"
    nameState="${name}_state.txt"
    mv $nameState "state.txt"
    newUrl=$(echo $line | sed "s/-[a-zA-Z0-9_]*.osm.pbf/-updates\//")
    sed -i "/^baseUrl=/c\baseUrl=$newUrl" configuration.txt
    osmosis --read-replication-interval workingDirectory="${deltDir}" --simplify-change --write-xml-change - | \
    osm2pgsql --append -r xml -s -C 300 -G --hstore --style openstreetmap-carto.style --tag-transform-script openstreetmap-carto.lua -d $DB_NAME -U $DB_USER -
    mv "state.txt" $nameState
done < ../src/links.config