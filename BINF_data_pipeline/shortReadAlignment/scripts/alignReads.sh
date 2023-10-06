#!/usr/bin/env bash
# alignReads.sh
# Usage: bash scripts/alignReads.sh 1>results/logs/alignReads.log 2>results/logs/alignReads.err &

function alignReads {
    local NAME=$1
    local SRR_ID=$2
    gsnap \
    -A sam \
    -D data \
    -d ${NAME}GmapDb \
    -N 1 \
    data/trimmed_data/${NAME}/${SRR_ID}.fastq \
    1>data/aligned_data/${NAME}/${NAME}.sam
}
alignReads $1 $2