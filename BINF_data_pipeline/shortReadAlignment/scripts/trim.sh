#!/usr/bin/env bash
# trim.sh

# path to the Trimmomatic program folder within our environment that contains the Illumina adapters

PATH_TO_TRIMMOMATIC="/shared/centos7/anaconda3/2021.11/envs/BINF-12-2021/pkgs/trimmomatic-0.39-hdfd78af_2/share/trimmomatic-0.39-2"
DATA_PATH="/home/gao.chenx/BINF_data_pipeline/shortReadAlignment/data"
function trim {
    local SRR_ID=$1
    local NAME=$2
    trimmomatic SE \
    -threads 1 -phred33 \
    $DATA_PATH/raw_data/${NAME}/${SRR_ID}.fastq \
    $DATA_PATH/trimmed_data/${NAME}/${SRR_ID}.fastq \
    HEADCROP:0 \
    ILLUMINACLIP:$PATH_TO_TRIMMOMATIC/adapters/TruSeq3-PE.fa:2:30:10 \
    LEADING:20 TRAILING:20 SLIDINGWINDOW:4:30 MINLEN:36
}
trim $1 $2