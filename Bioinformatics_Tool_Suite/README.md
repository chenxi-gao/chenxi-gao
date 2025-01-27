# Bioinformatics Tool Suite README

Welcome to the Bioinformatics Tool Suite! This collection comprises a range of scripts tailored to facilitate various operations related to genetic and protein data. This README provides a summarized overview of the tools available in this suite, alongside their core functionalities and usage instructions.

## 1. **Nucleotide Fasta Statistics** (`nt_fasta_stats.py`)
- **Purpose:** Computes statistics from nucleotide FASTA files, like sequence lengths and GC percentages.
- **Usage:** 
  ```bash
  $ python3 ./nt_fasta_stats.py --infile INPUT_FASTA_FILE --outfile OUTPUT_STATS_FILE
  ```
- **Output:** Tabulated statistics for each sequence, with details on nucleotide counts, sequence length, and GC percentage.
- **Detailed Document** [Nucleotide Fasta Statistics](./fasta_stats/README.md)

## 2. **Find Common Categories** (`find_common_cats.py`)
- **Purpose:** Identifies and describes common gene categories from two input files.
- **Usage:**
  ```bash
  $ python3 find_common_cats.py -i1 [PATH_TO_FILE1] -i2 [PATH_TO_FILE2]
  ```
- **Output:** Tabulated data of gene category occurrences and their descriptions.
- **Detailed Document** [Find Common Categories](./find_common_cats/README.md)

## 3. **Gene Names from Chromosome 21** (`gene_names_from_chr21.py`)
- **Purpose:** Allows users to query gene descriptions based on a gene symbol.
- **Usage:** 
  ```bash
  $ python3 gene_names_from_chr21.py -i [path_to_input_file]
  ```
- **Output:** Provides the description of the queried gene symbol.
- **Detailed Document** [Gene Names from Chromosome 21](./gene_names_from_chr21/README.md)

## 4. **Get Gene Level Information** (`get_gene_level_information.py`)
- **Purpose:** Retrieves tissue-specific gene expression data from the Unigene database.
- **Usage:**
  ```bash
  python get_gene_level_information.py --host [HOST_NAME] --gene [GENE_NAME]
  ```
- **Output:** Lists of tissues where a gene is expressed in the provided host.
- **Detailed Document** [Get Gene Level Information](./get_gene_level_information/README.md)

## 5. **Intersection of Gene Names** (`intersection_of_gene_names.py`)
- **Purpose:** Identifies common gene symbols between two input files.
- **Usage:**
  ```bash
  $ python3 intersection_of_gene_names.py -i1 [path_to_first_gene_list] -i2 [path_to_second_gene_list]
  ```
- **Output:** Number of unique and common gene symbols between two files, and a list of the common genes.
- **Detailed Document** [Intersection of Gene Names](./intersection_of_gene_names/README.md)

## 6. **Secondary Structure Splitter** (`secondary_structure_splitter.py`)
- **Purpose:** Separates amino acid sequences and their secondary structures from a FASTA format file.
- **Usage:** 
  ```bash
  $ python3 ./secondary_structure_splitter.py --infile [PATH_TO_INPUT_FILE]
  ```
- **Output:** Two FASTA files, one containing amino acid sequences (`pdb_protein.fasta`) and the other with the secondary structures (`pdb_ss.fasta`).
- **Detailed Document** [Secondary Structure Splitter](./ss_spliter/README.md)

## 7. **Add KEGG Pathways** (`addKEGGPathways.py`)

- **Purpose:** Appends KEGG (Kyoto Encyclopedia of Genes and Genomes) Ortholog ID, Pathway ID, and Pathway Description to each SwissProt (Uniprot) ID based on BLAST output, and allows filtering the BLAST output based on a specified e-value threshold.

- **Usage:** 
```sh
$ python3 addKEGGPathways.py --input [input_filename] --evalue [evalue_threshold] --output [output_filename]
```

- **Output:** Appends KEGG Ortholog ID, Pathway ID, and Pathway Description to the input data and writes the appended data to the specified output file.

- **Detailed Document** [Add KEGG Pathways README](./add_KEGG_pathways/README.md).

---

**Note:** It's always recommended to create backups of your data before running any script or operation. Ensure you have the necessary dependencies and Python environment setup to utilize the tools effectively. For detailed information, references, or troubleshooting, follow the respective "Detailed Documentation" links provided for each tool.

---

**Author:** Chenxi Gao

**Contact:** gao.chenx@northeastern.edu

**Version:** 1.0

**Last Updated:** 10-6-2023
