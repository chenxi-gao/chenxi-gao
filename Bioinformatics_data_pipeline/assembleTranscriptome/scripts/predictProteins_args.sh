#!/usr/bin/env bash
# predictProteins.sh
# Usage: bash scripts/predictProteins.sh 1>results/logs/predictProteins.log 2>results/logs/predictProteins.err

TransDecoder.Predict \
    -t $1 \
    -O $2 \
    --retain_pfam_hits $3 \
    --retain_blastp_hits $4