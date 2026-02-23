#!/bin/bash

set -ex

# Setup virtual environment
conda env create -f environment.yml

# Dependencies 
git submodule update --init --recursive

# Local Sample Data
zarr_folder="data/zarr"

if [ ! -d "${zarr_folder}" ] ; then
    ln -s "/fs/site5/eccc/cmd/s/sweb800/weong2zarr/maestro/weong2zarr/hub/ppp6/zarr/" "${zarr_folder}"
    echo "Sucessfully linked sample data: '${zarr_folder}'."
else
    echo "Sample data already linked: '${zarr_folder}'."
fi

# Local Storage Space
storage_folder="data/storage"

if [ ! -d "${storage_folder}" ] ; then

    read -p "The storage space is not linked yet. Do you want to create the link now? (y/n): " answer

    if [[ "$answer" == "y" || "$answer" == "Y" ]]; then
        ln -s "/fs/site5/eccc/mrd/rpnsi/$USER" "${storage_folder}"
        echo "Sucessfully linked storage space: '${storage_folder}'."
    else
        echo "Storage link creation skipped."
    fi
else
    echo "Storage space already linked: '${storage_folder}'."
fi
