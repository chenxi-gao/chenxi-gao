#!/usr/bin/env bash
# runTrinity.sh

NAME=$1
Trinity \
--genome_guided_bam data/bam/${NAME}/${NAME}.sorted.bam \
--genome_guided_max_intron 10000 \
--max_memory 10G --CPU 4 \
--output results/${NAME}/trinity_guided