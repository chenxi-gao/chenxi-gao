# Nucleotide Fasta Statistics (`nt_fasta_stats.py`)

## Overview

The `nt_fasta_stats.py` script processes a given FASTA file containing nucleotide sequences to calculate and report sequence lengths and the percentage of 'C' and 'G' bases for each sequence. The results are saved to an output file.

## Features

- Reads FASTA formatted files.
- Calculates the number of occurrences of each base (A, G, C, T, N) for every sequence.
- Computes the total length and GC percentage for every sequence.
- Outputs the statistics in a structured format.

## Requirements

- Python 3

## Usage

To execute the program, use the following command:

```
$ python3 ./nt_fasta_stats.py --infile INPUT_FASTA_FILE --outfile OUTPUT_STATS_FILE
```

Replace `INPUT_FASTA_FILE` with the path to your input FASTA file and `OUTPUT_STATS_FILE` with the desired name/path for the output statistics file.

For example:

```
$ python3 ./nt_fasta_stats.py --infile influenza.fasta --outfile influenza.stats.txt
```

## Output Format

The output file will contain a header followed by rows of data for each sequence in the FASTA file. Each row will provide the sequence number, NCBI accession number, counts of each nucleotide, total sequence length, and GC percentage.

```
Number   Accession     A's    G's    C's    T's    N's    Length    GC%
```

## Functions Overview

- `get_file_args()`: Parses command line arguments.
- `get_filehandle(filename, mode)`: Opens the provided file in the given mode and returns the file handle.
- `get_fasta_lists(filename)`: Processes a FASTA file and returns separate lists for headers and sequences.
- `output_seq_statistics(header_list, sequence_list, fh_out)`: Computes and writes the statistics to the output file.
- Helper functions to count bases, verify lists, extract NCBI accession numbers, etc.

## Note

Always ensure you have a backup of your files. Although the script is designed to read input files and not modify them, always be cautious when working with scripts and data.

## Authors

Chenxi Gao
gao.chenx@northeastern.edu

## Version History

* 0.1
    * Initial Release