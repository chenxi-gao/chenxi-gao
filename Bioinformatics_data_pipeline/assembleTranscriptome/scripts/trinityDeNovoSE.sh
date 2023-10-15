#!/usr/bin/env bash
# trinityDeNovo.sh

NAME=$1
SRR_ID=$2

Trinity \
--seqType fq \
--output results/${NAME}/trinity_de_novo \
--max_memory 10G --CPU 4 \
--single data/trimmed/${NAME}/${SRR_ID}.fastq