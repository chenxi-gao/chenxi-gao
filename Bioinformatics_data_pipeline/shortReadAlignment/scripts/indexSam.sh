#!/usr/bin/env bash
# indexSam.sh

NAME=$1
samtools index \
data/aligned_data/${NAME}/${NAME}.sorted.bam \