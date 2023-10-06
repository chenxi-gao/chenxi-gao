#!/usr/bin/env bash
# gmap_build.sh
NAME=$1
INPUT_PATH=$2
gmap_build -D data -d ${NAME}GmapDb ${INPUT_PATH}