#!/bin/bash

#SBATCH --job-name=FSI-test
#SBATCH --nodes=1
#SBATCH --ntasks=10
###SBATCH --ntasks-per-node=10
###SBATCH --gres=gpu:1
#SBATCH --partition=low
#SBATCH --output=job.log
#SBATCH --error=job.err
###SBATCH --begin=12:00
###SBATCH -t 24:00:00
###SBATCH --mem=220G

echo "--- This job is:$SLURM_JOB_NAME($SLURM_JOBID)"  
echo "--- Current working directory is:${PWD}"
echo "--- Running on ${NPROCS} processes (cores) on the following nodes:" 
echo "--- Starting job at:`date`"

export NPA=6
export NP=`echo $SLURM_TASKS_PER_NODE | cut -c1-2`
export NPF=$((NP)) 
export NODES=$(scontrol show hostnames)
export FLUID='Solution'
export STRUCT='Solution 1'

"$AWP_ROOT195/SystemCoupling/bin/systemcoupling" -R fsi.py

echo "--- Job finished at:`date`"
squeue | grep $SLURM_JOB_NAME | awk '{print "--- Total CPU hours:"$4}'
# date >> $HOME/sun/fluent_flag
