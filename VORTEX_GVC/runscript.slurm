#!/bin/bash
#SBATCH --job-name=VORTEX_GVC
#SBATCH --time=00:20:00
#SBATCH --account=\budget\account\code
#SBATCH --partition=standard
#SBATCH --qos=standard
#SBATCH --nodes=1
#SBATCH --ntasks-per-core=1
#SBATCH --cpus-per-task=1

# ARCHER2 support suggestion to reduce UCX error messages:
export UCX_IB_REG_METHODS=direct
export SRUN_CPUS_PER_TASK=$SLURM_CPUS_PER_TASK
. \path\to\modules\file

SHARED_ARGS="--distribution=block:block --hint=nomultithread"

#srun --het-group=0 --ntasks=4  ${SHARED_ARGS} ./nemo : \
# --het-group=1 --ntasks=1  ${SHARED_ARGS} ./xios_server.exe

srun --ntasks=4  ${SHARED_ARGS} ./nemo 

exit
