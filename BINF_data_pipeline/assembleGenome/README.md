## Genomic Data Analysis Pipeline

This document provides an overview and instructions for the Genomic Data Analysis Pipeline that downloads, trims, assembles, and analyzes Rhodobacter spheroides Next-Generation Sequencing (NGS) reads.

### Overview

The pipeline is structured in four main steps:
1. Downloading the NGS data using `fasterq-dump`.
2. Trimming the raw reads to remove any low-quality data using `trimmomatic`.
3. Assembling the trimmed reads using `spades.py` to construct the genome.
4. Analyzing the quality and statistics of the assembled genome using `quast.py`.

### Requirements

- SLURM job scheduler for managing the jobs.
- The Anaconda environment with the required tools (`fasterq-dump`, `trimmomatic`, `spades.py`, and `quast.py`) installed.

### Execution

Submit the main SLURM script (`sbatch_script_name.sh`) to SLURM:

```bash
sbatch sbatch_script_name.sh [NAME] [SRR_ID]
```

Replace `[NAME]` with the desired output name and `[SRR_ID]` with the specific SRR ID of the dataset.

example: 
```bash
sbatch sbatch_script_name.sh Rhodo SRR522244
```
```bash
sbatch sbatch_script_name.sh Yersinia SRR26255229
```

### Script Descriptions

1. **Main SLURM script (`sbatch_script_name.sh`):** This is the primary script that coordinates the entire pipeline. It accepts two arguments, NAME (name of the dataset or sample) and SRR_ID (unique identifier for the dataset on the SRA database).

2. **getNGS.sh:** Downloads NGS data using `fasterq-dump` from the SRA database.

   Usage:
   ```bash
   bash getNGS.sh [SRR_ID] [NAME]
   ```

3. **trim.sh:** Trims the raw reads using Trimmomatic to remove any adapters and low-quality data. It uses the Illumina adapter sequences for trimming.

   Usage:
   ```bash
   bash trim.sh [SRR_ID] [NAME]
   ```

4. **runSpades.sh:** Assembles the trimmed reads using `spades.py`.

   Usage:
   ```bash
   bash runSpades.sh [NAME] [SRR_ID]
   ```

5. **runQuast.sh:** Analyzes the quality of the assembled genome using `quast.py`.

   Usage:
   ```bash
   bash runQuast.sh [NAME]
   ```

### Output

All results and logs will be organized in the following directory structure:

```
|-- data/
|   |-- raw_data/
|   |-- trimmed_data/
|   |-- assembled_data/
|-- logs/
|-- quast_results/
```

- **data/raw_data/**: Contains downloaded NGS data.
- **data/trimmed_data/**: Contains trimmed reads.
- **data/assembled_data/**: Contains assembled genome sequences.
- **logs/**: Contains logs for each step in the pipeline, organized by job name and job ID.
- **quast_results/**: Contains results from the `quast.py` analysis.

### Notes

- Ensure that the Anaconda environment `BINF-12-2021` with all required tools is properly set up.
- Ensure that you have sufficient storage space and permissions to write to the specified directories.
- Always monitor the output logs to ensure that each step of the pipeline completes successfully.

## Authors

Chenxi Gao
gao.chenx@northeastern.edu

## Version History

* 0.1
    * Initial Release
