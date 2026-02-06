# RPN-PYGEOAPI

This repository provides tools for virtualizing and serving meteorological datasets using `pygeoapi`, `kerchunk`, and `virtualizarr`.

## Installation & Setup 

### 1. Initial Setup

Run this the first time you clone the repo to create the environment and install dependencies.

```bash
    # This script creates the venv and runs pip install
        # creates a symlink to sample data (`/zarr`)
    ./initial-setup.sh
```

### 2. Environment Activation

To work within the project, you must source the setup script. This ensures your shell is correctly configured.

```bash
    source setup.sh
```

### 3. Starting the Server

Once the environment is active, launch the `pygeoapi` server to expose your virtual datasets.

```bash
    ./bin/start-server.sh
```
