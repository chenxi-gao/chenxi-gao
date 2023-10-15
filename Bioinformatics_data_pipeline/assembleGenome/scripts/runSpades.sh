#!/usr/bin/env bash
# runSpades.sh
DATA_PATH="/home/gao.chenx/BINF_data_pipeline/assembleGenome/data"

function Spades {
    local NAME=$1
    local SRR_ID=$2
    spades.py \
    -1 $DATA_PATH/trimmed_data/${NAME}/${SRR_ID}.R1.paired.fastq \
    -2 $DATA_PATH/trimmed_data/${NAME}/${SRR_ID}.R2.paired.fastq \
    -o data/assembled_data/${NAME}
}

Spades $1 $2 # runs the function Spades