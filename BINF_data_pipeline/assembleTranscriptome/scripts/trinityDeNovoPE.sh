#!/usr/bin/env bash
# trinityDeNovo.sh

NAME=$1
SRR_ID=$2

Trinity \
--seqType fq \
--output results/${NAME}/trinity_de_novo \
--max_memory 10G --CPU 4 \
--left data/trimmed/${NAME}/${SRR_ID}.R1.paired.fastq \
--right data/trimmed/${NAME}/${SRR_ID}.R2.paired.fastq