#!/bin/bash                             
# tells the system that this is a bash file
#SBATCH --partition=short               # choose from debug, express, or short
#SBATCH --job-name=Rhodo
#SBATCH --time=04:00:00                 # the code pieces should run in far less than 4 hours
#SBATCH -N 1                            # nodes requested
#SBATCH -n 1                            # task per node requested
#SBATCH --output="batch-%x-%j.output"   # where to direct standard output; will be batch-jobname-jobID.output

echo "Starting our analysis $(date)"  

NAME="Rhodo"  # in future, we will define this as part of a config file
SRR_ID=SRR522244  # in future, we will define this as part of a config file

echo "$NAME SRR reads to process: $SRR_ID"

echo "Loading our BINF6308 Anaconda environment."
module load anaconda3/2021.11
source activate BINF-12-2021

echo "Create new folders for $NAME $(date)"
mkdir -p data/raw_data/$NAME
mkdir -p data/trimmed_data/$NAME
mkdir -p data/assembled_data/$NAME
mkdir -p logs/$SLURM_JOB_NAME-$SLURM_JOB_ID

echo "Downloading $SRR_ID reads $(date)"
bash scripts/getNGS.sh $SRR_ID $NAME 1>logs/$SLURM_JOB_NAME-$SLURM_JOB_ID/$SLURM_JOB_NAME-$SLURM_JOB_ID-getNGS.log 2>logs/$SLURM_JOB_NAME-$SLURM_JOB_ID/$SLURM_JOB_NAME-$SLURM_JOB_ID-getNGS.err

echo "Trimming $SRR_ID reads $(date)"
bash scripts/trim.sh $SRR_ID $NAME 1>logs/$SLURM_JOB_NAME-$SLURM_JOB_ID/$SLURM_JOB_NAME-$SLURM_JOB_ID-trim.log 2>logs/$SLURM_JOB_NAME-$SLURM_JOB_ID/$SLURM_JOB_NAME-$SLURM_JOB_ID-trim.err

echo "Assembling genome from trimmed $SRR_ID reads $(date)"
bash scripts/runSpades.sh $NAME $SRR_ID 1>logs/$SLURM_JOB_NAME-$SLURM_JOB_ID/$SLURM_JOB_NAME-$SLURM_JOB_ID-runSpades.log 2>logs/$SLURM_JOB_NAME-$SLURM_JOB_ID/$SLURM_JOB_NAME-$SLURM_JOB_ID-runSpades.err

echo "Analyzing genome assembly $(date)"
bash scripts/runQuast.sh $NAME 1>logs/$SLURM_JOB_NAME-$SLURM_JOB_ID/$SLURM_JOB_NAME-$SLURM_JOB_ID-runQuast.log 2>logs/$SLURM_JOB_NAME-$SLURM_JOB_ID/$SLURM_JOB_NAME-$SLURM_JOB_ID-runQuast.err

echo "Assembly and analysis complete $(date)"