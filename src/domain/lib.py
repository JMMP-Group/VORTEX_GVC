#!/usr/bin/env python

from typing import Optional

from os.path import isfile, basename, splitext
import numpy as np
import xarray as xr
from xarray import DataArray, Dataset

def generate_hgrid(
    ppe1_m,
    ppe2_m,
    jpiglo,
    jpjglo,
    chunks: Optional[dict] = None,
) -> Dataset:
    """
    Generate coordinates and spacing of the NEMO VORTEX test-case.
    The grid is centred around a T-point at the middle of the domain 
    (hence domain size is odd).

    Parameters
    ----------
    ppe1_m, ppe2_m: float, 1D array-like
        Grid spacing along x/y axis (units: m).
    jpiglo, jpjglo: int, optional
        Size of x/y dimension.
    chunks: dict, optional
         Chunk sizes along each dimension (e.g., ``{"x": 5, "y": 5}``).
         Requires ``dask`` installed.

    Returns
    -------
    Dataset
        Equivalent of NEMO coordinates file.

    Raises
    ------
    ValueError
        If ``ppe{1,2}_m`` is a vector and ``jp{i,j}glo`` is specified, or viceversa.

    Notes
    -----
    Vectors are loaded into memory. If ``chunks`` is specified, 2D arrays are coerced
    into dask arrays before broadcasting.
    """

    ds = Dataset()
    for dim, ppe, jp in zip(
        ["x", "y"], [ppe1_m, ppe2_m], [jpiglo, jpjglo]
    ):

        # Check and convert ppe to numpy array
        ppe = np.asarray(ppe, dtype=float)
        if (ppe.shape and jp) or (not ppe.shape and not jp):
            raise ValueError(
                "`jp{i,j}glo` must be specified"
                " if and only if `ppe{1,2}_m` is not a vector."
            )


        ppg = -0.5*ppe + (-jp)*0.5*ppe # written as in NEMO
        # c: center f:face
        delta_c = DataArray(ppe if ppe.shape else ppe.repeat(jp), dims=dim)
        coord_c = ppg + delta_c.cumsum(dim)
        coord_f = coord_c.rolling({dim:2}).mean().shift({dim:-1}).fillna(coord_c[-1]+0.5*ppe)
        delta_f = coord_c.diff(dim).pad({dim: (0, 1)}, constant_values=delta_c[-1])

        # Add attributes
        for da in [coord_c, coord_f]:
            da.attrs = dict(
                units="km", long_name=f"{dim}-coordinate in Cartesian system"
            )
        for da in [delta_c, delta_f]:
            da.attrs = dict(units="m", long_name=f"{dim}-axis spacing")

        # Fill dataset
        eprefix = "e" + ("1" if dim == "x" else "2")
        gprefix = "g" + ("lam" if dim == "x" else "phi")
        nav_coord = "nav_" + ("lon" if dim == "x" else "lat")
        vel_c = "v" if dim == "x" else "u"
        vel_f = "v" if dim == "y" else "u"
        ds[nav_coord] = ds[gprefix + "t"] = ds[gprefix + vel_c] = coord_c / 1000.
        ds[gprefix + "f"] = ds[gprefix + vel_f] = coord_f / 1000.
        ds[eprefix + "t"] = ds[eprefix + vel_c] = delta_c
        ds[eprefix + "f"] = ds[eprefix + vel_f] = delta_f

        # Upgrade dimension to coordinate so we can add CF-attributes
        ds[dim] = ds[dim]
        ds[dim].attrs = dict(axis=dim.upper(), long_name=f"{dim}-dimension index")

    # Generate 2D coordinates (create dask arrays before broadcasting).
    # Order dims (y, x) for convenience (e.g., for plotting).
    (ds,) = xr.broadcast(ds if chunks is None else ds.chunk(chunks))
    ds = ds.transpose(*("y", "x"))

    return ds.set_coords(ds.variables)

class Bathymetry:
    """
    Class to generate idealized test bathymetry datasets.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize class generating NEMO Cartesian grid.

        Parameters
        ----------
        *args
            Arguments passed on to :py:func:`pydomcfg.utils.generate_cartesian_grid`
        *kwargs
            Keyword arguments passed on to
            :py:func:`pydomcfg.utils.generate_cartesian_grid`.
        """
        self._coords = generate_hgrid(*args, **kwargs)

    def flat(self, depth: float) -> Dataset:
        """
        Flat bottom case.

        Parameters
        ----------
        depth: float
            Bottom depth (units: m).

        Returns
        -------
        Dataset
        """
        ds = self._coords
        ds["Bathymetry"] = xr.full_like(ds["glamt"], depth)
        return ds

    def sea_mount(self, 
                  glamt_mid: float, 
                  gphit_mid: float, 
                  bot_max: float, 
                  smnt_H: float, 
                  smnt_L: float
                 ) -> Dataset:
        """
        Gaussian seamount case as in Ezer et al 2002.

        Parameters
        ----------
        i_mid: int
            i-index of the centre of the seamount (units: None)
        j_mid: int
            j-index of the centre of the seamount (units: None)
        bot_max: float
            Maximum bottom topography depth (units: m).
        smnt_H: float
            Height of the seamount (units: m)
        smnt_L: float
            Width of the seamount (units: m)

        Returns
        -------
        Dataset
        """
        ds = self._coords

        #glamt_mid, gphit_mid = (g.isel({'x': i_mid, 'y': j_mid}) for g in (ds.glamt, ds.gphit))

        # Define sea mount bathymetry
        ds["Bathymetry"] = bot_max - smnt_H * np.exp(
                           -((1000. * (ds.glamt - glamt_mid))**2 + 
                             (1000. * (ds.gphit - gphit_mid))**2 )  
                           / (1000. * smnt_L)**2 )

        return ds

