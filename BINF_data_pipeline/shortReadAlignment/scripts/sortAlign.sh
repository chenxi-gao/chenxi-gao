#!/usr/bin/env bash
# sortAlign.sh

NAME=$1
samtools sort \
data/aligned_data/${NAME}/${NAME}.sam \
-o data/aligned_data/${NAME}/${NAME}.sorted.bam \