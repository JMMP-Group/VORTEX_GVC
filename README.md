# VORTEX_GVC
Work to develop and test methods for changing the type of GVC in AGRIF nests

## Setting up the conda env
'''
conda env create -f pyogcm.yml
conda activate pyogcm
'''

## How to use it

```
nemo_dir=\path\to\your\local\NEMO\checkout
cp ref_cfgs.txt ${nemodir}/cfgs
cp -r VORTEX_GVC cfgs
# On MetOffice HPC
source ${nemodir}/ukmo_utils/use_intel_hpc.sh
./makenemo -r VORTEX_GVC -m XC40_METO_IFORT
```
