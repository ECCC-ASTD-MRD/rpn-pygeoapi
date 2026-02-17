#!/bin/bash
#set -e

# Python 3.12
#source r.load.dot eccc/cmd/cmds/env/python/py312_2025.9.0_all

# Virtual environment
#python3 -m venv venv
#source venv/bin/activate

# Dependencies 
git submodule update --init --recursive

pip install --upgrade pip
pip install -r requirements.txt

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

# ===== GDAL ===== #
#pip uninstall -y gdal
#pip uninstall -y mapscript

exit

module avail gcc    # optional: to view available modules
module load gcc/15.1.0

module avail gdal   # optional: to view available modules
module load gdal/3.11.0

pip install gdal==3.11.0

# In case 'pip install' throws DISK QUOTA Exceeded Error 
# export TMPDIR=/fs/site5/eccc/mrd/rpnsi/ibb000
