## Next-Generation Sequencing Data Analysis Pipelines

This document provides an overview and instructions for three main pipelines used for the analysis of Next-Generation Sequencing (NGS) data. The pipelines cater to genomic, transcriptomic, and RNAseq alignment data. Each pipeline is designed to process data, trim the reads, and align or assemble them as per the requirements.

![flowchart](https://github.com/chenxi-gao/workSample/blob/main/BINF_data_pipeline/BINF_data_pipeline.png)

### 1. Genomic Data Analysis Pipeline

- **Objective:** Download, trim, assemble, and analyze Rhodobacter spheroides NGS reads.
- **Main Steps:** Data Download → Trimming → Genome Assembly → Genome Quality Analysis
- **Key Tools:** `fasterq-dump`, `trimmomatic`, `spades.py`, `quast.py`
- **Execution Command:**
  ```bash
  sbatch sbatch_script_name.sh [NAME] [SRR_ID]
  ```
  [Genomic Data Analysis Pipeline](./assembleGenome/README.md)

### 2. Transcriptome Analysis Pipeline

- **Objective:** Download, trim, assemble, and analyze Sinorhizobium NGS transcriptomic data.
- **Main Steps:** Data Download → Trimming → De Novo Assembly → Transcriptome Quality Analysis → ORF Prediction & Alignment
- **Key Tools:** `fasterq-dump`, `trimmomatic`, `Trinity`, `TransDecoder`, `hmmscan`, `blastp`
- **Execution Command:**
  ```bash
  sbatch sbatch_transcriptome.sh [NAME] [SRR_ID]
  ```
  [Transcriptome Analysis Pipeline](./assembleTranscriptome/README.md)

### 3. RNAseq Alignment Pipeline

- **Objective:** Process RNA sequencing data, trim reads, and align to a reference genome.
- **Main Steps:** Data Download → Reference Genome Building → Trimming → Read Alignment → SAM Sorting → BAM Indexing
- **Key Tools:** `fasterq-dump`, `trimmomatic`, `gsnap`, `samtools`
- **Execution Command:**
  ```bash
  sbatch sbatch_alignRNAseq.sh [NAME] [SRR_ID]
  ```
  [RNAseq Alignment Pipeline](./shortReadAlignment/README.md)

---

## Directory Structure

The general directory structure for output and logs across all pipelines:

```
|-- data/
|   |-- raw_data/
|   |-- trimmed_data/
|   |-- assembled_data/  (For Genomic & Transcriptomic Pipelines)
|   |-- aligned_data/    (For RNAseq Alignment Pipeline)
|-- logs/
|-- results/
```

---

## Authors

Chenxi Gao  

gao.chenx@northeastern.edu

## Version History

* 0.1
    * Initial Release of all three pipelines.

---

### Note to Users:
- It's essential to ensure that the Anaconda environment with all required tools is correctly set up for the respective pipelines.
- Always monitor the output logs to ensure each step completes successfully.
- Ensure sufficient storage space and appropriate write permissions.
- For in-depth details of each pipeline, please refer to their dedicated README sections.

---

### Detailed Pipeline Instructions:

[Genomic Data Analysis Pipeline](./assembleGenome/README.md)

[Transcriptome Analysis Pipeline](./assembleTranscriptome/README.md)

[RNAseq Alignment Pipeline](./shortReadAlignment/README.md)
