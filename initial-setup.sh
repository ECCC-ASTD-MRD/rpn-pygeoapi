#!/bin/bash
set -e

# --- 1. Python 3.12 ---
source r.load.dot eccc/cmd/cmds/env/python/py312_2025.9.0_all

# --- 2. Workspace Environment ---
python3 -m venv venv
source venv/bin/activate

# --- 3. Dependencies --- 
git submodule update --init --recursive

pip install --upgrade pip
pip install -r requirements.txt

# --- 4. Configuration File ---
if [ ! -f "example-config.yml" ] ; then
    cp pygeoapi/pygeoapi-config.yml pygeoapi/example-config.yml
fi
