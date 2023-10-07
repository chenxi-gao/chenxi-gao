## README for `get_gene_level_information.py`

### Overview:

The `get_gene_level_information.py` script is designed to retrieve data from the Unigene database. It accepts input for both host and gene names, and it returns information about in which tissues the specified gene is expressed for the given host.

### Prerequisites:

1. **Python Environment**: Ensure that you have Python 3.x installed.
2. **Required Libraries**: 
   - `sys`
   - `re`
   - `argparse`
   
Ensure you also have the `config` and `io_utils` modules available in the same directory as this script or in your Python path.

### Usage:

```bash
python get_gene_level_information.py --host [HOST_NAME] --gene [GENE_NAME]
```

#### Arguments:

- `--host`: The name of the host. This is case-insensitive, and can be either in common or scientific name format. If the scientific name contains spaces, ensure it's enclosed in double quotes. Default value is 'Human'.

- `-g` or `--gene`: The name of the gene you're interested in. Default value is 'A1BG'.

### Functionality:

1. **Standardizes Input Host Name**: It takes the provided host name and checks it against available conversions from common to scientific names.

2. **File Verification**: Before processing, the script checks the existence of the gene file in the directory specified by the configuration.

3. **Data Retrieval**: If the file exists, the script extracts a list of tissues in which the specified gene is expressed.

4. **Output**: The final output is a list of tissues where the gene is expressed in the provided host.

### Errors and Exceptions:

If the script can't find the specified host name in its database, it will display a list of available hosts both by their scientific and common names before exiting. If the gene file doesn't exist for the given host, the script will notify the user and terminate.

### Note:

Ensure your configuration in `config.py` is correctly set up, particularly the directory and file extension for Unigene data.

If you experience any issues or have feature requests, please raise them with the maintainer or check the documentation for further details.

## Authors

Chenxi Gao
gao.chenx@northeastern.edu

## Version History

* 0.1
    * Initial Release
