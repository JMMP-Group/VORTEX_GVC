#!/usr/bin/env python

from os.path import isfile, basename, splitext
import numpy as np
from matplotlib import pyplot as plt
import xarray as xr

# Load hgrid
hgrd = "/data/users/dbruciaf/VORTEX_GVC/vortex_input_files/coordinates.nc"
ds_hgrd = xr.open_dataset(hgrd)
bathy = ds_hgrd.e1t.copy()*0. + 5000.
ds_hgrd["Bathymetry"] = bathy
ds_hgrd = ds_hgrd.drop(["e1t","e2t","e1u","e2u","e1v","e2v","e1f","e2f",
                        "glamt","glamu","glamv","glamf","gphit","gphiu","gphiv","gphif"
                       ])

# -------------------------------------------------------------------------------------   
# Writing the bathy_meter.nc file

out_file = "/data/users/dbruciaf/VORTEX_GVC/vortex_input_files/bathy_flat.nc"
ds_hgrd.to_netcdf(out_file)
