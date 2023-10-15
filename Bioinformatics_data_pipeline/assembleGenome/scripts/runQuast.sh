#!/usr/bin/env bash
# runQuast.sh

function Quast {
    quast.py data/assembled_data/"$1"/contigs.fasta -o quast_results/"$1"
}

Quast $1