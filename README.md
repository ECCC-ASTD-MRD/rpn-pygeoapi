# RPN-PYGEOAPI

Exposing meteorological research datasets using `pygeoapi`.

## 🎯 Objectives

To facilitate access to meteorological data, this project aims:

- **To serve** geospatial data through a web interface.
- **To create** virtual subsets of large datasets.
- **To avoid** data duplication.

## ⚙️ Stack

* **Core:** `pygeoapi`
* **Data Handling:** Currently experimenting with `kerchunk`

## 🚀 Setup & Run

### 1. Install Prerequisites

Run this once to set up the environment and dependencies.

```bash
    # additionally creates a symlink to sample data (`/zarr`)
    ./initial-setup.sh
```

### 2. Activate Environment

To work within the project, you must source the setup script. This ensures your shell is correctly configured.

```bash
    source setup.sh
```

### 3. Start The Server

Once the environment is active, launch the `pygeoapi` server to expose your virtual datasets.

```bash
    ./bin/start-server.sh
```
