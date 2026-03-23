import xarray as xr

vds = xr.open_dataset("2026010700_000", engine="fstd")

vds.to_zarr("2026010700_000.zarr")
