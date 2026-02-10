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


## Retrieving Datasets

To avoid exceeding your storage quota, you'll to create a symlink as such:

```bash
    ln -s /fs/site5/eccc/mrd/rpnsi/$USER my_storage_space
```

Once that's done, you'll be able to run heavy scripts like `share/rpn-pygeoapi/fetch-data.py`.
