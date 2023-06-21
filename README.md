# VORTEX_GVC
Work to develop and test methods for changing the type of GVC in AGRIF nests

## Setting up the conda env
```
conda env create -f pyogcm.yml
conda activate pyogcm
```

## How to use it

### On MetOffice HPC
```
nemo_dir=\path\to\your\local\NEMO\checkout
cp ref_cfgs.txt ${nemodir}/cfgs
cp -r VORTEX_GVC cfgs
source ${nemodir}/ukmo_utils/use_intel_hpc.sh
./makenemo -r VORTEX_GVC -m XC40_METO_IFORT
```

To run the VORTEX_GVC `cd cfgs/VORTEX_GVC/EXP00`. An example submission script is here: `../run_job.sh`

### On ARCHER2 HPC

```
git clone git@github.com:JMMP-Group/VORTEX_GVC.git
. ./VORTEX_GVC/env/gnu-mpich
git clone  https://forge.nemo-ocean.eu/nemo/nemo.git nemo
svn co http://forge.ipsl.jussieu.fr/ioserver/svn/XIOS/trunk@2479 xios
cd xios
export XIOS_DIR=$PWD
cp ../VORTEX_GVC/arch/xios/arch-archer2-gnu-mpich.* arch/
./make_xios --full --prod --arch archer2-gnu-mpich --netcdf_lib netcdf4_par --job 10
cd ../nemo
git checkout aafd62a791c3377cf4395ca940a057d74223f1a0
cp -r ../VORTEX_GVC/VORTEX_GVC ./cfgs/
cp -r ../VORTEX_GVC/ref_cfgs.txt ./cfgs/
cp ../VORTEX_GVC/arch/nemo/arch-archer2-gnu-mpich.fcm arch/
sed -i "s?XXX_XIOS_DIR_XXX?$XIOS_DIR?" ./arch/arch-archer2-gnu-mpich.fcm
./makenemo -r VORTEX_GVC -m archer2-gnu-mpich -j 14
```

To run the VORTEX_GVC `cd cfgs/VORTEX_GVC/EXP00`. An example submission script is here: `../runscript.slurm`
