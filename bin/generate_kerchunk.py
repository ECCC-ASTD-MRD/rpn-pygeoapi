#!/usr/bin/env python3

import os
import glob
import xarray as xr
import ujson
from virtualizarr import open_virtual_dataset
from kerchunk.combine import MultiZarrToZarr
from kerchunk.zarr import single_zarr

ZARR_DIR = 'zarr/vof-wings'
OUTPUT_JSON = './combined.json'

def create_merged_index():
    zarr_files = sorted(glob.glob(f"{ZARR_DIR}/*.zarr"))
    
    single_indexes = []
    
    for f in zarr_files:
        try:
            ds = single_zarr(
                f,
                inline_threshold=0
            )
            single_indexes.append(ds)
        except Exception as e:
            print("Error", e)
            continue
            
    # urls = [f"file://{f}" for f in zarr_files]
    
    mzz = MultiZarrToZarr(
        single_indexes,
        remote_protocol='file',
        concat_dims=['time'],
        identical_dims=['lat', 'lon', 'height', 'y', 'x']
    )
    
    dico_fusionne = mzz.translate()
    
    with open(OUTPUT_JSON, 'w') as f:
        ujson.dump(dico_fusionne, f)

create_merged_index()
