#!/usr/bin/env bash
# pfamScan.sh
# Usage: bash scripts/pfamScan.sh 1>results/logs/pfamScan.log 2>results/logs/pfamScan.err

hmmscan --cpu 4 --domtblout $1 $2 $3