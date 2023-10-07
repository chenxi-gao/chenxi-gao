# Find Common Categories

## Overview

The `find_common_cats.py` script processes two input files containing genes and their associated categories, and then outputs the occurrence count of each category along with its description. This tool is especially useful for researchers and bioinformaticians looking to analyze the distribution of gene categories based on the data from the input files.

## Dependencies

- Python 3.x
- `collections`
- `argparse`
- `get_file.io_utils` (ensure the module and its function `get_filehandle` are available)

## Usage

You can execute the script using the following command:

```bash
$ python3 find_common_cats.py -i1 [PATH_TO_FILE1] -i2 [PATH_TO_FILE2]
```

Replace `[PATH_TO_FILE1]` and `[PATH_TO_FILE2]` with the paths to your input files. 

### Input Files

1. `chr21_genes.txt` (or equivalent file specified by `-i1`): This file should contain gene data including the category for each gene.
2. `chr21_genes_categories.txt` (or equivalent file specified by `-i2`): This file should map gene categories to their descriptions.

The script expects the data in these files to be tab-separated.

### Output

The script will generate an output file named `categories.txt` in the `OUTPUT` directory. This file will have three columns: `Category`, `Occurrence`, and `Description`, representing the gene category, its occurrence count, and its description respectively.

## Function Descriptions

- `get_file_args()`: Parses the command line arguments for the input files.
- `get_cat_num(fh_gen)`: Returns a dictionary mapping gene categories to their counts based on the data from the first input file.
- `get_cat_des_dict(fh_cat)`: Returns a dictionary mapping gene categories to their descriptions based on the data from the second input file.

## Authors

Chenxi Gao
gao.chenx@northeastern.edu

## Version History

* 0.1
    * Initial Release
