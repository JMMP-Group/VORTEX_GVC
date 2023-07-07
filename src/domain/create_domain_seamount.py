#!/usr/bin/env python

from os.path import isfile, basename, splitext
from lib import generate_hgrid, Bathymetry


# VORTEX configuration

bot_max = 5000.    # Maximum depth of the domain
smnt_H = 2400.     # Height of the seamount
smnt_L = 80.       # Width of the seamount
i_mid = 23         # i-index of the seamount centre in the parent grid
j_mid = 22         # j-index of the seamount centre in the parent grid

ppe1_m_p = 30000.0 # zonal grid-spacing of parent domain
ppe2_m_p = 30000.0 # merid grid-spacing of parent domain
Ni0glo_p = 63      # 1st dimension of parent domain
Nj0glo_p = 63      # 2nd dimension of parent domain

refx_c = 3         # space refinement factor of the child grid in x direction
refy_c = 3         # space refinement factor of the child grid in y direction
Ni0glo_c = 65      # 1st dimension of child domain
Nj0glo_c = 65      # 2nd dimension of child domain

# Generate parent domain

ds_parent = generate_hgrid(ppe1_m_p, ppe2_m_p, Ni0glo_p, Nj0glo_p)
out_file  = "/data/users/dbruciaf/VORTEX_GVC/vortex_input_files/coordinates.nc"
ds_parent.to_netcdf(out_file)

glamt_mid, gphit_mid = (g.isel({'x': i_mid, 'y': j_mid}) for g in (ds_parent.glamt, ds_parent.gphit))

ds_parent = Bathymetry(ppe1_m_p, ppe2_m_p, Ni0glo_p, Nj0glo_p)
ds_parent = ds_parent.sea_mount(glamt_mid, gphit_mid, bot_max, smnt_H, smnt_L)
out_file  = "/data/users/dbruciaf/VORTEX_GVC/vortex_input_files/seamount/bathy_meter.nc"
ds_parent.to_netcdf(out_file)

# Generate child domain

ds_child = generate_hgrid(ppe1_m_p / refx_c, ppe2_m_p / refy_c, Ni0glo_c, Nj0glo_c)
out_file = "/data/users/dbruciaf/VORTEX_GVC/vortex_input_files/1_coordinates.nc"
ds_child.to_netcdf(out_file)

ds_child = Bathymetry(ppe1_m_p / refx_c, ppe2_m_p / refy_c, Ni0glo_c, Nj0glo_c)
ds_child = ds_child.sea_mount(glamt_mid, gphit_mid, bot_max, smnt_H, smnt_L)
out_file  = "/data/users/dbruciaf/VORTEX_GVC/vortex_input_files/seamount/1_bathy_meter.nc"
ds_child.to_netcdf(out_file)

