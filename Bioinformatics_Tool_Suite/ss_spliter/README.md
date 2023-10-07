## Secondary Structure Splitter

### Overview:

The `secondary_structure_splitter.py` script processes a FASTA format file containing information on amino acid sequences and their respective secondary structures. The script will generate two output files. One of these output files contains the amino acid sequences, while the other contains the secondary structure, both in FASTA format.

### Usage:

```bash
$ python3 ./secondary_structure_splitter.py --infile [PATH_TO_INPUT_FILE]
```

Where `[PATH_TO_INPUT_FILE]` should be replaced with the path to your input file.

### Example:

```bash
$ python3 ./secondary_structure_splitter.py --infile ss.txt
```

### Outputs:

The script produces two output files:

1. `pdb_protein.fasta` : Contains the amino acid sequences.
2. `pdb_ss.fasta` : Contains the secondary structures.

### Functions:

1. `get_file_args()` : Retrieves command-line arguments.
2. `get_filehandle(filename, mode)` : Opens the file for reading or writing.
3. `get_fasta_lists(filename)` : Separates headers and sequences from the FASTA file.
4. `_verify_lists(header_list, sequence_list)` : Helper function to ensure that the length of headers and sequences lists are the same.
5. `output_result_to_file(header_list, seq_list, fh_out1, fh_out2)` : Writes the separated sequences and secondary structures to their respective files.

### Error Handling:

- If there's an issue opening the file, an error will be raised indicating either a non-existent file or an incorrect open mode.
- If the lengths of the headers and sequences do not match, the script will print an error message and exit.

### Notes:

Ensure that the input file is in the correct format for optimal results. Always back up your data before running scripts or operations on your files.

## Authors

Chenxi Gao
gao.chenx@northeastern.edu

## Version History

* 0.1
    * Initial Release
