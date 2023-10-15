#!/usr/bin/bash
#SBATCH --partition=short               # choose from debug, express, or short
#SBATCH --job-name=alignRNAseq
#SBATCH --time=01:00:00                 # the code pieces should run in far less than 1 hour
#SBATCH -N 1                            # nodes requested
#SBATCH -n 1                            # task per node requested
#SBATCH --output="batch-%x-%j.output"   # where to direct standard output; will be batch-jobname-jobID.output

# Usage: sbatch sbatch_alignRNAseq.sh 

NAME=$1  # in future, we will define this as part of a config file
SRR_ID=$2  # in future, we will define this as part of a config file
GMAPDb_PATH="/home/gao.chenx/BINF_data_pipeline/assembleGenome/data/assembled_data/Rhodo/contigs.fasta"

echo "Starting our analysis $(date)"  

echo "Loading our BINF6308 Anaconda environment."
module load anaconda3/2021.11
source activate BINF-12-2021
echo "Loading GSNAP and Samtools."
module load gsnap/2021-12-17
module load samtools/1.10

echo "Create a new folder for the $NAME $(date)"
mkdir -p data/raw_data/$NAME
mkdir -p data/trimmed_data/$NAME
mkdir -p data/aligned_data/$NAME
mkdir -p logs/$SLURM_JOB_NAME-$SLURM_JOB_ID

echo "Downloading the $SRR_ID reads RNA seq $(date)"
bash scripts/getNGS.sh $SRR_ID $NAME 1>results/logs/$SLURM_JOB_NAME-$SLURM_JOB_ID/$SLURM_JOB_NAME-$SLURM_JOB_ID-getNGS.log 2>results/logs/$SLURM_JOB_NAME-$SLURM_JOB_ID/$SLURM_JOB_NAME-$SLURM_JOB_ID-getNGS.err

echo "Build the reference genome $(date)"
bash scripts/gmap_build.sh $NAME $GMAPDb_PATH 1>logs/$SLURM_JOB_NAME-$SLURM_JOB_ID/$SLURM_JOB_NAME-$SLURM_JOB_ID-gmap_build.log 2>logs/$SLURM_JOB_NAME-$SLURM_JOB_ID/$SLURM_JOB_NAME-$SLURM_JOB_ID-gmap_build.err

echo "Trim all $NAME reads in data/raw_data/ $(date)"
bash scripts/trim.sh $SRR_ID $NAME 1>logs/$SLURM_JOB_NAME-$SLURM_JOB_ID/$SLURM_JOB_NAME-$SLURM_JOB_ID-trim.log 2>logs/$SLURM_JOB_NAME-$SLURM_JOB_ID/$SLURM_JOB_NAME-$SLURM_JOB_ID-trim.err

echo "Align the reads to the reference with GSNAP $(date)"
bash scripts/alignReads.sh $NAME $SRR_ID 1>logs/$SLURM_JOB_NAME-$SLURM_JOB_ID/$SLURM_JOB_NAME-$SLURM_JOB_ID-alignReads.log 2>logs/$SLURM_JOB_NAME-$SLURM_JOB_ID/$SLURM_JOB_NAME-$SLURM_JOB_ID-alignReads.err

echo "Sort the resulting SAM files $(date)"
bash scripts/sortAlign.sh $NAME 1>logs/$SLURM_JOB_NAME-$SLURM_JOB_ID/$SLURM_JOB_NAME-$SLURM_JOB_ID-sortAlign.log 2>logs/$SLURM_JOB_NAME-$SLURM_JOB_ID/$SLURM_JOB_NAME-$SLURM_JOB_ID-sortAlign.err

echo "Index the resulting BAM files $(date)"
bash scripts/indexSam.sh $NAME 1>logs/$SLURM_JOB_NAME-$SLURM_JOB_ID/$SLURM_JOB_NAME-$SLURM_JOB_ID-indexSam.log 2>logs/$SLURM_JOB_NAME-$SLURM_JOB_ID/$SLURM_JOB_NAME-$SLURM_JOB_ID-indexSam.err

echo "Alignment complete $(date)"
