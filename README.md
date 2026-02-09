# RPN-PYGEOAPI

A lightweight server specifically designed to expose meteorological research data using 'pygeoapi'.

## Objectives

To facilitate access to meteorological data, this project aims:

- **To serve** geospatial data dynamically through a web interface.
- **To create** virtual subsets  of large datasets.
- **To avoid** data duplication of heavy storage redundancy.

## Setup & Run

### Installation

Run this once to set up the environment and dependencies.

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
