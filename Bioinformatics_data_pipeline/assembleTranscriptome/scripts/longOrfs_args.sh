#!/usr/bin/env bash
# longOrfs.sh
# Usage: bash scripts/longOrfs.sh 1>results/logs/longOrfs.log 2>results/logs/longOrfs.err

TransDecoder.LongOrfs -t $1 -O $2 