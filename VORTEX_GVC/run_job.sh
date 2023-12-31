#!/bin/bash --login

#PBS -N VORTEX
#PBS -l walltime=02:00:00
#PBS -j oe
#PBS -q normal
#PBS -l select=1
#PBS -P jmmp

  export PBS_O_WORKDIR=$(readlink -f $PBS_O_WORKDIR)
  export OMP_NUM_THREADS=1
  cd $PBS_O_WORKDIR

  ulimit -c unlimited
  ulimit -s unlimited

  OCORES=4
  O_PER_NODE=4
  #OCORES=1
  #O_PER_NODE=1

  echo "time aprun -b -n ${OCORES} -N ${O_PER_NODE} ./nemo" 
  time aprun -b -n ${OCORES} -N ${O_PER_NODE} ./nemo

