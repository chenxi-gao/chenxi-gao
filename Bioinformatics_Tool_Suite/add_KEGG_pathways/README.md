# README for `addKEGGPathways.py`

## Description

`addKEGGPathways.py` is a Python script designed to append KEGG (Kyoto Encyclopedia of Genes and Genomes) Ortholog ID, Pathway ID, and Pathway Description to each SwissProt (Uniprot) ID, based on BLAST output. It also allows filtering the BLAST output based on a specified e-value threshold.

## Prerequisites

Before you begin, ensure you have met the following requirements:
- **Python 3**: You need Python 3 to run `addKEGGPathways.py`. Download it from [here](https://www.python.org/downloads/).
- **requests**: This Python library is used for making HTTP requests. You can install it using pip:
  ```sh
  pip install requests
  ```

## Usage

### Command Line
The script can be run from the command line with optional arguments:

```sh
$ python3 addKEGGPathways.py --input [input_filename] --evalue [evalue_threshold] --output [output_filename]
```

### Arguments
- `--input` or `-i`: Specifies the input filename (default: `alignPredicted.txt`).
- `--evalue` or `-e`: Specifies the e-value threshold for filtering the BLAST output (default: `1e-50`).
- `--output` or `-o`: Specifies the output filename (default: `alignPredicted_addKEGGPathways.txt`).

### Example
```sh
$ python3 addKEGGPathways.py --input alignPredicted.txt --evalue 1e-50 --output alignPredicted_addKEGGPathways.txt
```

## Functionality

1. **Input File**: Takes an input file containing BLAST output and an optional e-value threshold.
   
2. **Filtering**: Extracts UniProt IDs from the input file, filtering by the provided e-value threshold.
   
3. **KEGG Data Retrieval**: For each UniProt ID:
   - Converts UniProt ID to KEGG gene ID using the KEGG API.
   - Retrieves corresponding KEGG Orthology ID.
   - Retrieves corresponding KEGG Pathway IDs.
   
4. **Appending Data**: Appends KEGG Ortholog ID, Pathway ID, and Pathway Description to the input data.

5. **Output File**: Writes the appended data to the specified output file.

## Output Format

The script generates an output file with additional columns appended to each line of the input file:

```
[Input Line] [KEGG Ortholog ID] [KEGG Pathway ID] [KEGG Pathway Description]
```
## Example input:
```
TRINITY_DN21437_c0_g1_i1.p1     sp|Q13496|METN_CERS4  132     603     132     82      62.121  1.84e-60        RecName: Full=Myotubularin; AltName: Full=Phosphatidylinositol-3,5-bisphosphate 3-phosphatase; AltName: Full=Phosphatidylinositol-3-phosphate phosphatase
```
## Example output:
```
TRINITY_DN21437_c0_g1_i1.p1     sp|Q13496|METN_CERS4  132     603     132     82      62.121  1.84e-60        RecName: Full=Myotubularin; AltName: Full=Phosphatidylinositol-3,5-bisphosphate 3-phosphatase; AltName: Full=Phosphatidylinositol-3-phosphate phosphatase   ko:K01108 path:ko00562  Inositol phosphate metabolism
TRINITY_DN21437_c0_g1_i1.p1     sp|Q13496|METN_CERS4  132     603     132     82      62.121  1.84e-60        RecName: Full=Myotubularin; AltName: Full=Phosphatidylinositol-3,5-bisphosphate 3-phosphatase; AltName: Full=Phosphatidylinositol-3-phosphate phosphatase   ko:K01108 path:ko01100  Metabolic pathways
TRINITY_DN21437_c0_g1_i1.p1     sp|Q13496|METN_CERS4  132     603     132     82      62.121  1.84e-60        RecName: Full=Myotubularin; AltName: Full=Phosphatidylinositol-3,5-bisphosphate 3-phosphatase; AltName: Full=Phosphatidylinositol-3-phosphate phosphatase   ko:K01108 path:ko04070  Phosphatidylinositol signaling system
```

## Note

- Ensure your internet connection is stable, as the script retrieves data from the KEGG API.
- Be mindful of the usage policy of KEGG API to prevent IP blocking due to excessive access.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgements

- [KEGG API Documentation](https://www.kegg.jp/kegg/rest/keggapi.html)

## Support

If you have any questions or encounter any issues, please open an issue in the GitHub repository.

---

**Disclaimer**: Ensure to comply with the usage and redistribution policy of the data retrieved from KEGG or any other databases. Always cite the respective databases in your research publications.
