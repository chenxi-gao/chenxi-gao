#!/usr/bin/env bash
# blastPep.sh
# Usage: bash scripts/blastPep.sh 1>results/blastPep.outfmt6 2>results/logs/blastPep.err

blastp -query $1  \
    -db $2 \
    -max_target_seqs 1 \
    -outfmt 6 -evalue 1e-5 -num_threads 4 