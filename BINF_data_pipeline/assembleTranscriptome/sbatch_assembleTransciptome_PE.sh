#!/usr/bin/bash
#SBATCH --partition=short               # choose from debug, express, or short
#SBATCH --job-name=Sinorhizobium
#SBATCH --time=20:00:00                 # the code pieces should run in far less than 1 hour
#SBATCH -N 1                            # nodes requested
#SBATCH -n 4                            # task per node requested
#SBATCH --mem=10Gb
#SBATCH --exclusive
#SBATCH --output="batch-%x-%j.output"   # where to direct standard output; will be batch-jobname-jobID.output
#SBATCH --mail-type=ALL
#SBATCH --mail-user=gao.chenx@northeastern.edu

# Usage: sbatch sbatch_transcriptome.sh

NAME=$1
SRR_ID=$2

echo "Starting our analysis $(date)"  

echo "Loading our BINF6308 Anaconda environment, which includes Trinity."
module load anaconda3/2021.11
source activate BINF-12-2021
echo "Loading samtools."
module load samtools/1.10

echo "Make directory for data files"
mkdir -p data/raw_data/${NAME}
mkdir -p data/trimmed/${NAME}
mkdir -p results/logs/$SLURM_JOB_NAME-$SLURM_JOB_ID

echo "Downloading $SRR_ID reads $(date)"
bash scripts/getNGS.sh $SRR_ID $NAME 1>results/logs/$SLURM_JOB_NAME-$SLURM_JOB_ID/$SLURM_JOB_NAME-$SLURM_JOB_ID-getNGS.log 2>results/logs/$SLURM_JOB_NAME-$SLURM_JOB_ID/$SLURM_JOB_NAME-$SLURM_JOB_ID-getNGS.err

echo "Trimming $SRR_ID reads $(date)"
bash scripts/trimPE.sh $SRR_ID $NAME 1>results/logs/$SLURM_JOB_NAME-$SLURM_JOB_ID/$SLURM_JOB_NAME-$SLURM_JOB_ID-trimPE.log 2>results/logs/$SLURM_JOB_NAME-$SLURM_JOB_ID/$SLURM_JOB_NAME-$SLURM_JOB_ID-trimPE.err

echo "Starting De Novo Assembly $(date)"
echo "Assemble the De Novo Transcriptome $(date)"
bash scripts/trinityDeNovoPE.sh $NAME $SRR_ID 1>results/logs/$SLURM_JOB_NAME-$SLURM_JOB_ID/$SLURM_JOB_NAME-$SLURM_JOB_ID-trinityDeNovoPE.log 2>results/logs/$SLURM_JOB_NAME-$SLURM_JOB_ID/$SLURM_JOB_NAME-$SLURM_JOB_ID-trinityDeNovoPE.err

echo "Analyze the De Novo Transcriptome $(date)"
bash scripts/analyzeTrinityDeNovo.sh $NAME 1>results/$NAME/$SLURM_JOB_NAME-$SLURM_JOB_ID-trinity_de_novo_stats.txt 2>results/logs/$SLURM_JOB_NAME-$SLURM_JOB_ID/$SLURM_JOB_NAME-$SLURM_JOB_ID-analyzeTrinityDeNovo.err

echo "De Novo Assembly complete $(date)"

echo "Assemblies complete $(date)"

echo "Starting our analysis $(date)" 

TRANSCRIPTOME=results/$NAME/trinity_de_novo/Trinity.fasta
SWISSPROT_DB=/home/gao.chenx/BINF_data_pipeline/assembleTranscriptome/data/blastDB/swissProt
TRANSDECODER_DIR=results/$NAME/trinity_de_novo.transdecoder_dir
LONGEST_ORFS=$TRANSDECODER_DIR/longest_orfs.pep
OUTFMT=results/$NAME/blastPep_args.outfmt6
DOMTBLOUT=results/$NAME/pfam.domtblout
PFAMA_PATH=/home/gao.chenx/BINF_data_pipeline/assembleTranscriptome/data/Pfam/Pfam-A.hmm
PREDICTED_PROTEIN_PATH=results/$NAME/predictedProteins
FINAL_PROTEINS=$PREDICTED_PROTEIN_PATH/*transdecoder.pep


echo "Starting ORF prediction pipeline $(date)"
echo "Identify longORFs with TransDecoder.LongOrfs on $TRANSCRIPTOME $(date)"
bash scripts/longOrfs_args.sh $TRANSCRIPTOME $TRANSDECODER_DIR \
  1>results/logs/$SLURM_JOB_NAME-$SLURM_JOB_ID/$SLURM_JOB_NAME-$SLURM_JOB_ID-longOrfs_args.log \
  2>results/logs/$SLURM_JOB_NAME-$SLURM_JOB_ID/$SLURM_JOB_NAME-$SLURM_JOB_ID-longOrfs_args.err

echo "BLASTp of longest_orfs.pep against SwissProt BLAST DB at $SWISSPROT_DB $(date)"
bash scripts/blastPep_args.sh $LONGEST_ORFS $SWISSPROT_DB \
  1>$OUTFMT \
  2>results/logs/$SLURM_JOB_NAME-$SLURM_JOB_ID/$SLURM_JOB_NAME-$SLURM_JOB_ID-blastPep_args.err

echo "Create pfamScan with hmmscan using the Pfam-A.hmm file found $PFAMA_PATH $(date)"
bash scripts/pfamScan_args.sh $DOMTBLOUT $PFAMA_PATH $LONGEST_ORFS \
  1>results/logs/$SLURM_JOB_NAME-$SLURM_JOB_ID/$SLURM_JOB_NAME-$SLURM_JOB_ID-pfamScan_args.log \
  2>results/logs/$SLURM_JOB_NAME-$SLURM_JOB_ID/$SLURM_JOB_NAME-$SLURM_JOB_ID-pfamScan_args.err

echo "Predict protiens with TransDecoder.Predict $(date)"
bash scripts/predictProteins_args.sh $TRANSCRIPTOME $TRANSDECODER_DIR $DOMTBLOUT $OUTFMT \
  1>results/logs/$SLURM_JOB_NAME-$SLURM_JOB_ID/$SLURM_JOB_NAME-$SLURM_JOB_ID-predictProteins_args.log \
  2>results/logs/$SLURM_JOB_NAME-$SLURM_JOB_ID/$SLURM_JOB_NAME-$SLURM_JOB_ID-predictProteins_args.err
echo "Copy TransDecoder.Predict outputs to $PREDICTED_PROTEIN_PATH"
mkdir -p $PREDICTED_PROTEIN_PATH
mv *transdecoder* $PREDICTED_PROTEIN_PATH

echo "Align predicted proteins to SwissProt DB $(date)"
bash scripts/alignPredicted_args.sh $FINAL_PROTEINS $SWISSPROT_DB \
  1>results/$NAME/alignPredicted.txt \
  2>results/logs/$SLURM_JOB_NAME-$SLURM_JOB_ID/$SLURM_JOB_NAME-$SLURM_JOB_ID-alignPredicted_args.err

echo "ORF prediction pipeline complete $(date)"

echo "Analysis complete $(date)"
