# Gene Names from Chromosome 21 Script

## Description

This script allows users to query gene descriptions based on a gene symbol. The data is sourced from an input file, and the gene description corresponding to the input gene symbol is displayed to the user.

For example, given a file containing gene symbols and their descriptions, the program will prompt the user to enter a gene symbol. If the gene exists in the file, its description will be printed. The user can continue querying for gene symbols until they decide to exit the program.

## Requirements

- Python 3.x
- The `get_file.io_utils` library (or make sure that the `get_filehandle` function is available in the mentioned module)

## Usage

To execute the program, use the following command:

```
$ python3 gene_names_from_chr21.py -i [path_to_input_file]
```

Replace `[path_to_input_file]` with the path to the gene data file. The gene data file should be formatted with gene names in the first column and descriptions in the second column, separated by tabs. The first line (header) of the file will be skipped.

## Example

Assuming the script is run with a `chr21_genes.txt` input file like this:

```
GeneSymbol    Description
GENE1         This is a description for gene 1.
GENE2         This is a description for gene 2.
```

When the script is executed:

```
$ python3 gene_names_from_chr21.py -i chr21_genes.txt
```

The user will be prompted:

```
Enter gene name of interest. Type quit to exit:
```

On entering `GENE1`, the script will display:

```
GENE1 found! Here is the description:
This is a description for gene 1.
```

The user can continue querying for other gene symbols or type `quit` to exit the program.

## Authors

Chenxi Gao

gao.chenx@northeastern.edu

## Version History

* 0.1
    * Initial Release
