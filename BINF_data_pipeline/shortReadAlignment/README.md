## RNAseq Alignment Pipeline

This document provides an overview and instructions for the RNAseq Alignment Pipeline. The pipeline processes RNA sequencing data, trims the reads, and aligns them to a reference genome.

### Overview

The pipeline is composed of seven main steps:
1. Downloading the RNAseq data using `fasterq-dump`.
2. Building the reference genome using `gmap_build`.
3. Trimming the raw reads using `trimmomatic`.
4. Aligning the reads to the reference genome with `gsnap`.
5. Sorting the resulting SAM files using `samtools`.
6. Indexing the resulting BAM files using `samtools`.
7. Completing the alignment.

### Requirements

- SLURM job scheduler for managing the jobs.
- The Anaconda environment with the necessary tools (`fasterq-dump`, `trimmomatic`, `gsnap`, and `samtools`) installed.

### Execution

Submit the main SLURM script (`sbatch_alignRNAseq.sh`) to SLURM:

```bash
sbatch sbatch_alignRNAseq.sh [NAME] [SRR_ID]
```

Replace `[NAME]` with the desired output name and `[SRR_ID]` with the specific SRR ID of the dataset.

example:
```bash
sbatch sbatch_alignRNAseq.sh Rhodo SRR21973231
```

### Script Descriptions

1. **Main SLURM script (`sbatch_alignRNAseq.sh`):** The master script that manages the entire pipeline. It takes two arguments, NAME (dataset or sample name) and SRR_ID (unique identifier for the dataset on the SRA database).

2. **getNGS.sh:** Downloads RNAseq data using `fasterq-dump` from the SRA database.

   Usage:
   ```bash
   bash getNGS.sh [SRR_ID] [NAME]
   ```

3. **gmap_build.sh:** Builds the reference genome.

   Usage:
   ```bash
   bash gmap_build.sh [NAME] [INPUT_PATH]
   ```

4. **trim.sh:** Trims the raw reads using Trimmomatic.

   Usage:
   ```bash
   bash trim.sh [SRR_ID] [NAME]
   ```

5. **alignReads.sh:** Aligns the reads to the reference genome using `gsnap`.

   Usage:
   ```bash
   bash alignReads.sh [NAME] [SRR_ID]
   ```

6. **sortAlign.sh:** Sorts the SAM file using `samtools`.

   Usage:
   ```bash
   bash sortAlign.sh [NAME]
   ```

7. **indexSam.sh:** Indexes the BAM file using `samtools`.

   Usage:
   ```bash
   bash indexSam.sh [NAME]
   ```

### Output

All results and logs are organized within the following directory structure:

```
.
├── batch-alignRNAseq-38927891.output
├── data
│   ├── aligned_data
│   │   └── Rhodo
│   │       ├── Rhodo.sam
│   │       ├── Rhodo.sorted.bam
│   │       └── Rhodo.sorted.bam.bai
│   ├── raw_data
│   │   └── Rhodo
│   │       └── SRR21973231.fastq
│   ├── RhodoGmapDb
│   │   └── ...
│   └── trimmed_data
│       └── Rhodo
│           └── SRR21973231.fastq
├── logs
│   └── alignRNAseq-38927891
│       └── ...
├── sbatch_alignRNAseq_Rhodo_SRR21973231.sh
└── scripts
    ├── alignReads.sh
    ├── getNGS.sh
    ├── gmap_build.sh
    ├── indexSam.sh
    ├── sortAlign.sh
    └── trim.sh
```

- **data/raw_data/**: Contains downloaded RNAseq data.
- **data/trimmed_data/**: Contains trimmed reads.
- **data/aligned_data/**: Contains aligned reads in SAM and BAM formats.
- **logs/**: Contains logs for each step in the pipeline, organized by job name and job ID.
- **results/**: Contains result files from various steps.

### Notes

- Ensure that the Anaconda environment `BINF-12-2021` with all required tools is properly set up.
- Ensure that you have sufficient storage space and permissions to write to the specified directories.
- Always monitor the output logs to verify that each step of the pipeline completes successfully.

## Authors

Chenxi Gao
gao.chenx@northeastern.edu

## Version History

* 0.1
    * Initial Release
