# VORTEX_GVC
Work to develop and test methods for changing the type of GVC in AGRIF nests

## Setting up the conda env
```
conda env create -f pyogcm.yml
conda activate pyogcm
```

## How to use it

```
nemo_dir=\path\to\your\local\NEMO\checkout
cp ref_cfgs.txt ${nemodir}/cfgs
cp -r VORTEX_GVC cfgs
# On MetOffice HPC
source ${nemodir}/ukmo_utils/use_intel_hpc.sh
./makenemo -r VORTEX_GVC -m XC40_METO_IFORT
```

## On ARCHER2 HPC

```
git clone git@github.com:JMMP_Group/VORTEX_GVC.git
git clone  https://forge.nemo-ocean.eu/nemo/nemo.git nemo
git checkout aafd62a791c3377cf4395ca940a057d74223f1a0
cd nemo
cp -r ../VORTEX_GVC/VORTEX_GVC ./cfgs/
cp -r ../VORTEX_GVC/ref_cfgs.txt ./cfgs/
. ../VORTEX_GVC/arch/gnu-mpich
./makenemo -r VORTEX_GVC -m gnu-mpich
```
