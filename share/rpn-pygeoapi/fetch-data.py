# Script pour récupérer des données publiques du web (L'hypothèse qu'elles seraient plus stables que celles du CMC)
# URL: https://console.cloud.google.com/storage/browser/gcp-public-data-arco-era5/ar/1959-2022-6h-1440x721.zarr

import xarray as xr
import gcsfs
import asyncio
from pathlib import Path
from tqdm.dask import TqdmCallback
import pandas

current_file = Path(__file__).resolve()
project_dir = current_file.parents[2]

async def read_data():
    fs = gcsfs.GCSFileSystem(token='anon', asynchronous=True)
    store = fs.get_mapper('gs://gcp-public-data-arco-era5/ar/1959-2022-6h-1440x721.zarr') 
    
    ds = xr.open_zarr(store, consolidated=True)
    
    ds_slice = ds.sel(
                        time=slice('2020-01-01T00:00:00','2020-01-01T18:00:00'),                        
                        longitude=slice(20,40)
                      )
    print(ds_slice.time)
    
    with TqdmCallback(desc="Download ERA5 Data"):
        ds_slice.to_zarr(f"./data/era5.zarr", mode='w', zarr_format=2, compute=True)


asyncio.run(read_data())
