# Chenxi Gao's Work Sample Repository

This repository encompasses a diverse range of projects and scripts, providing a comprehensive view of Chenxi Gao's expertise in areas such as cloud-based data processing, next-generation sequencing, bioinformatics, and molecular prediction using machine learning.

## Table of Contents
1. [AWS-based Stream Data Pipeline and Data Analyze](https://github.com/chenxi-gao/workSample/tree/main/AWS_stream_data_pipeline)
2. [Next-Generation Sequencing Data Analysis Pipelines](https://github.com/chenxi-gao/workSample/tree/main/BINF_data_pipeline)
3. [Bioinformatics Tool Suite](https://github.com/chenxi-gao/workSample/tree/main/Bioinformatics_Tool_Suite)
4. [Molecular Prediction Jupyter Notebook](https://github.com/chenxi-gao/workSample/tree/main/machine_learning_GNN)

---

## AWS-based Stream Data Pipeline and Data Analyze

- **Description:** A project showcasing the use of AWS services to process and analyze pizza-related data.
- **Key Features:** State-wise data reporting on top-selling pizzas, high-speed data querying, and integration with external data sources.
- **Technologies:** Amazon Redshift, AWS API Gateway, Lambda, Kinesis Data Firehose, AWS Glue, RDS MySQL.
- **Documentation & Details:** [AWS-based Stream Data Pipeline](https://www.notion.so/TORQATA-PIZZA-BUSINESS-7375585a4b3e4d7c9d028f9c4261bc9b)
  
  ![flowchart](https://github.com/chenxi-gao/workSample/blob/main/AWS_stream_data_pipeline/workflow_torqata.png)

---

## Next-Generation Sequencing Data Analysis Pipelines

- **Description:** Overview and instructions for three main pipelines designed for genomic, transcriptomic, and RNAseq alignment data analysis.
- **Key Steps:** Data Downloading, Trimming, Assembly or Alignment, and Data Analysis.
- **Technologies:** `fasterq-dump`, `trimmomatic`, `Trinity`, `TransDecoder`, `hmmscan`, `blastp`, and others.
- **Detailed Pipelines:** [Genomic](./BINF_data_pipeline/assembleGenome/README.md), [Transcriptomic](./BINF_data_pipeline/assembleTranscriptome/README.md), and [RNAseq Alignment](./BINF_data_pipeline/shortReadAlignment/README.md).
  
  [flowchart](https://github.com/chenxi-gao/workSample/blob/main/BINF_data_pipeline/BINF_data_pipeline.png)

---

## Bioinformatics Tool Suite

- **Description:** A suite of scripts for various bioinformatics operations such as FASTA file statistics, finding common gene categories, and splitting protein sequences based on secondary structures.
- **Key Tools:** `nt_fasta_stats.py`, `find_common_cats.py`, `gene_names_from_chr21.py`, `get_gene_level_information.py`, `intersection_of_gene_names.py`, `secondary_structure_splitter.py`.
- **Detailed Instructions:** Check individual tool READMEs provided in the respective links.

    [Nucleotide Fasta Statistics](./Bioinformatics_Tool_Suite/fasta_stats/README.md)
  
    [Find Common Categories](./Bioinformatics_Tool_Suite/find_common_cats/README.md)
  
    [Gene Names from Chromosome 21](./Bioinformatics_Tool_Suite/gene_names_from_chr21/README.md)
  
    [Get Gene Level Information](./Bioinformatics_Tool_Suite/get_gene_level_information/README.md)
  
    [Intersection of Gene Names](./Bioinformatics_Tool_Suite/intersection_of_gene_names/README.md)
  
    [Secondary Structure Splitter](./Bioinformatics_Tool_Suite/ss_spliter/README.md)

---

## Molecular Prediction Jupyter Notebook

- **Description:** A Jupyter notebook workflow that predicts molecular properties using graph-based neural networks with the PyTorch Geometric library.
- **Key Steps:** Library Imports, Data Loading, Neural Network Model Definition, Training Loop, and Evaluation.
- **Technologies:** `RDKit`, `Torch`, `Torch Geometric`, `MoleculeNet`, `Pandas`, `Seaborn`.
- **Documentation & Details:** [GNN](https://github.com/chenxi-gao/workSample/blob/main/machine_learning_GNN/README.md)


---

### Contact

**Chenxi Gao**  

Email: gao.chenx@northeastern.edu

### License & Version

This repository is open-source and free to use under standard licenses. Always ensure the compatibility of libraries and tools for your use case.

Current Version: 0.1

---

### Note

While going through the work samples, users are advised to refer to detailed READMEs or documentation provided for each project to get a deeper understanding. This README serves as a summarized overview of the rich portfolio of projects and tools contained within the repository.
