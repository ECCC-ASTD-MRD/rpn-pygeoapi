#!/bin/bash
set -e

# Python 3.12
source r.load.dot eccc/cmd/cmds/env/python/py312_2025.9.0_all

# Virtual environment
python3 -m venv venv
source venv/bin/activate

# Dependencies 
git submodule update --init --recursive

pip install --upgrade pip
pip install -r requirements.txt

# Local Sample Data
zarr_folder="zarr"

if [ ! -d "${zarr_folder}" ] ; then
    ln -s "/fs/site5/eccc/cmd/s/sweb800/weong2zarr/maestro/weong2zarr/hub/ppp6/zarr/" "${zarr_folder}"
    echo "Les collections de fichiers zarr ont été créées avec succès."
else
    echo "Le sous-répertoire 'zarr' existe déjà."
fi
