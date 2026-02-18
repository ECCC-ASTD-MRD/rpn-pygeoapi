# RPN-PYGEOAPI

This project serves meteorological research data using `pygeoapi`.

## 🎯 Objectives

To facilitate access to research data, this project aims:

- **To serve** meteorological data through a web interface.
- **To create** virtual subsets of large datasets.
- **To avoid** data duplication.

## ⚙️ Stack

* **Core:** [`pygeoapi`](https://github.com/geopython/pygeoapi)
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

This operation is necessary to retrieve public datasets like _ERA5_ from the web.

## Installing GDAL

If you encounter the `no gdal-config found` error, you may need to manually load the required modules. 
This issue could also be due to a mismatch between the installed GDAL version and your Python environment.

### Option 1 — Load System Modules

```bash
module avail gcc    # optional: to view available modules
module load gcc/15.0.1

module avail gdal   # optional: to view available modules
module load gdal/3.11.0

pip install gdal==3.11
```

### Option 2 — Use Conda (Preferred)

Using `conda` is generally more reliable, especially when working with C-based dependencies like GDAL, as it avoids 
common OS-level conflicts. 

```bash
    conda install -c conda-forge GDAL MapServer
```
## 🌐 Hosting on the Web

This section concerns the deployment of the API on the institutional `web.science.gc.ca`.

To ease HTTP access to the `pygeoapi` REST endpoints, a symbolic link has been created from the server's web root.
This setup enables client-side web request to reach the running `pygeoapi` API without duplicating files or modifying 
the core project.

```bash
    ln -s ~/public_html var/www
```


## Documenting API Requests


### Dataset 1 - Public Zarr ERA5

- http://localhost:5000/collections/public-zarr/coverage?f=json&bbox=-90,-90,90,90&properties=10m_u_component_of_wind&datetime=2020-01-01T00:00:00/2020-01-01T00:00:00

