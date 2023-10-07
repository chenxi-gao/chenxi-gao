# SBATCH Script README

## Overview
This repository contains an SBATCH script for a bioinformatics pipeline designed to process and analyze Next Generation Sequencing (NGS) data. The script primarily focuses on handling reads from the organism "Rhodo", though the code structure permits scalability for other organisms in the future. The process includes data retrieval, trimming, genome assembly, and assembly analysis.

## Files Included:
1. **Main SBATCH Script**: The master script that dictates the workflow, manages resources, and initiates the subscripts.
2. **getNGS.sh**: Retrieves the NGS reads using `fasterq-dump`.
3. **trim.sh**: Trims the raw reads using `Trimmomatic` to remove any undesirable sequences or low-quality reads.
4. **runSpades.sh**: Assembles the trimmed reads into a genome using the `SPAdes` genome assembler.
5. **runQuast.sh**: Analyzes the quality of the assembled genome using `Quast`.

## Usage:

### 1. Submission:
Submit the main SBATCH script to an SLURM job scheduler using the command:
```bash
sbatch [SBATCH_SCRIPT_NAME].sh
```

### 2. Directories & Naming:
By default, the organism's name is set as "Rhodo" and its corresponding SRR ID as "SRR522244". The data for each organism is organized into separate directories (e.g., raw_data, trimmed_data, assembled_data) for clarity.

### 3. Output:
All standard outputs and errors from each step are redirected to respective log files under the `logs/` directory, named according to the pattern: `[JOB_NAME]-[JOB_ID]-[STAGE].log` and `[JOB_NAME]-[JOB_ID]-[STAGE].err`.

### 4. Dependencies:
The script assumes the availability of:
- Anaconda environment with specific modules (Anaconda3/2021.11) loaded.
- Pre-installed tools within the conda environment: `fasterq-dump`, `Trimmomatic`, `SPAdes`, and `Quast`.

## Modifications:
To adapt the script for another organism:
- Update the `NAME` variable with the new organism's name.
- Update the `SRR_ID` variable with the appropriate Sequence Read Archive (SRA) ID.
- Ensure that all data paths and directory structures match your environment.

## Important Notes:
- Always backup your data before running any new script or making changes.
- Regularly monitor log files to ensure that the pipeline runs smoothly without errors.
- If using the script in a different environment, ensure all dependencies are correctly installed and paths are correctly specified.

## Authors

Chenxi Gao
gao.chenx@northeastern.edu

## Version History

* 0.1
    * Initial Release
