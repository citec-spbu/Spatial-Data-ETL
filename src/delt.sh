#!/bin/bash
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
    OIFS=$IFS
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
    IFS=$OIFS
    newUrl="https://download.geofabrik.de/russia/"$name"fed-district-updates/"
    echo $newUrl
    sed -i "/^baseUrl=/c\baseUrl=$newUrl" configuration.txt
    osmosis --read-replication-interval workingDirectory="${deltDir}" --simplify-change --write-xml-change - | \
    osm2pgsql --append -r xml -s -C 300 -G --hstore --style openstreetmap-carto.style --tag-transform-script openstreetmap-carto.lua -d $DB_NAME -U $DB_USER -
done < ../src/links.config