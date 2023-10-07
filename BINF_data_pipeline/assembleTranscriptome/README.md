## Transcriptome Analysis Pipeline

This document provides an overview and instructions for the Transcriptome Analysis Pipeline that downloads, trims, assembles, and analyzes Sinorhizobium NGS transcriptomic data.

### Overview

The pipeline is structured in several main steps:
1. Downloading the NGS transcriptomic data using `fasterq-dump`.
2. Trimming the raw reads using `trimmomatic`.
3. De Novo assembly of the trimmed reads using `Trinity`.
4. Analyzing the quality and statistics of the assembled transcriptome.
5. Predicting Open Reading Frames (ORFs) and aligning predicted proteins against a reference database.

### Requirements

- SLURM job scheduler for managing the jobs.
- The Anaconda environment with the required tools (`fasterq-dump`, `trimmomatic`, `Trinity`, `TransDecoder`, `hmmscan`, `blastp`) installed.

### Execution

Submit the main SLURM script to SLURM:

```bash
sbatch sbatch_transcriptome_SE.sh [NAME] [SRR_ID]
```
```bash
sbatch sbatch_transcriptome_PE.sh [NAME] [SRR_ID]
```

Replace `[NAME]` with the desired output name and `[SRR_ID]` with the specific SRR ID of the dataset.

Example:
```bash
sbatch sbatch_transcriptome_SE.sh Rhodo SRR21973231
```
```bash
sbatch sbatch_transcriptome_PE.sh Sinorhizobium ERR11631749
```

### Script Descriptions

1. **Main SLURM script:** This is the primary script that coordinates the entire pipeline. It accepts two arguments, NAME (name of the dataset or sample) and SRR_ID (unique identifier for the dataset on the SRA database).

2. **getNGS.sh:** Downloads NGS transcriptomic data using `fasterq-dump` from the SRA database.

   Usage:
   ```bash
   bash getNGS.sh [SRR_ID] [NAME]
   ```

3. **trimPE.sh:** Trims the raw reads using Trimmomatic.

   Usage:
   ```bash
   bash trimPE.sh [SRR_ID] [NAME]
   ```

4. **trinityDeNovo.sh:** De Novo assembly of the trimmed reads using `Trinity`.

   Usage:
   ```bash
   bash trinityDeNovoPE.sh [NAME] [SRR_ID]
   ```

5. **analyzeTrinityDeNovo.sh:** Analyzes the quality of the assembled transcriptome.

   Usage:
   ```bash
   bash analyzeTrinityDeNovo.sh [NAME]
   ```

6. **longOrfs.sh:** Predicts long ORFs using `TransDecoder.LongOrfs`.

   Usage:
   ```bash
   bash longOrfs_args.sh [TRANSCRIPTOME] [TRANSDECODER_DIR]
   ```

7. **blastPep.sh:** Runs BLASTp for the predicted peptides against a reference database.

   Usage:
   ```bash
   bash blastPep_args.sh [LONGEST_ORFS] [SWISSPROT_DB]
   ```

8. **pfamScan.sh:** Scans for protein families using `hmmscan` against the Pfam database.

   Usage:
   ```bash
   bash pfamScan_args.sh [DOMTBLOUT] [PFAMA_PATH] [LONGEST_ORFS]
   ```

9. **predictProteins.sh:** Predicts proteins from the ORFs using `TransDecoder.Predict`.

   Usage:
   ```bash
   bash predictProteins_args.sh [TRANSCRIPTOME] [TRANSDECODER_DIR] [DOMTBLOUT] [OUTFMT]
   ```

10. **alignPredicted_args.sh:** Aligns the predicted proteins against the SwissProt database.

    Usage:
    ```bash
    bash alignPredicted_args.sh [FINAL_PROTEINS] [SWISSPROT_DB]
    ```

### Output

All results and logs will be organized in the following directory structure:

```
|-- data/
|   |-- raw_data/
|   |-- trimmed/
|-- results/
|   |-- logs/
|   |-- [NAME]/
|       |-- trinity_de_novo/
|       |-- trinity_de_novo.transdecoder_dir/
|       |-- blastPep_args.outfmt6/
|       |-- pfam.domtblout/
|       |-- predictedProteins/
```

### Notes

- Ensure that the Anaconda environment `BINF-12-2021` with all required tools is properly set up.
- Always monitor the output logs to ensure that each step of the pipeline completes successfully.
- Ensure you have the necessary reference databases and files, such as SwissProt and Pfam databases.
- Make sure to check the storage space requirements before running, especially for De Novo transcriptome assembly and ORF prediction, as they can generate substantial data.

## Authors

Chenxi Gao
gao.chenx@northeastern.edu

## Version History

* 0.1
    * Initial Release
