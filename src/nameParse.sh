#!/bin/bash
IFS='/' read -r -a wordsArr <<< "$line"
    len=${#wordsArr[@]}
    nameArr=( "${wordsArr[@]:3:${len}}" )
    echo "${nameArr[@]}"
    name=""
    for word in "${nameArr[@]}";
    do
        word=$(echo $word | sed "s/-[a-zA-Z0-9_]*.osm.pbf//")
        name="${name}${word}_"
    done
    name=${name%?}