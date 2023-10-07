# Intersection of Gene Names

## Description

`intersection_of_gene_names.py` is a Python script designed to identify common gene symbols between two input files. The script will output the number of unique gene names in each file, the number of common gene symbols found, and a list of these common genes. The results will be both displayed on the console and written to an output file (`OUTPUT/intersection_output.txt`).

## Requirements

- Python 3
- `get_file.io_utils` module (specifically the `get_filehandle` function)

## Usage

To execute the script, use the following command:

```bash
$ python3 intersection_of_gene_names.py -i1 [path_to_first_gene_list] -i2 [path_to_second_gene_list]
```

For example:

```bash
$ python3 intersection_of_gene_names.py -i1 test_data/chr21_genes.txt -i2 test_data/HUGO_genes.txt
```

### Arguments:

- `-i1` or `--file1`: Path to the first gene list file.
- `-i2` or `--file2`: Path to the second gene list file.

Both arguments are mandatory.

## Output

The script will produce an output file named `intersection_output.txt` in the `OUTPUT` directory. The file will contain the number of unique gene names in both input files and the number of common gene symbols found. The console will display the names of the common genes.

For instance, the output file might have content such as:

```
Number of unique gene names in chr21_genes.txt: 100
Number of unique gene names in HUGO_genes.txt: 150
Number of common gene symbols found: 50
Output stored in OUTPUT/intersection_output.txt
```

While the console will display the list of common genes.

## Important Notes

1. Ensure the `OUTPUT` directory exists or modify the script to create one if not.
2. The script assumes that the gene names in the input files are present in the first column.

## Authors

Chenxi Gao
gao.chenx@northeastern.edu

## Version History

* 0.1
    * Initial Release
