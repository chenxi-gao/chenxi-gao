#!/usr/bin/env bash
# getNGS.sh

# Retrieve the Rhodobacter spheroides NGS reads.
fasterq-dump --split-3 $1 -O data/raw_data/"$2"
