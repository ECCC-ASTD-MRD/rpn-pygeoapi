# RPN-PYGEOAPI

Serve meteorological research data through [`pygeoapi`](https://github.com/geopython/pygeoapi), with support for Zarr format.

## 🎯 Objectives

To facilitate access to research data, this project aims:

- **To serve** gridded data through a web interface.
- **To create** virtual subsets of large datasets.
- **To avoid** data duplication.

## 🚀 Setup and Run

### 1. Install Dependencies

Run this once to set up the environment and dependencies.

```bash
    ./initial-setup.sh
```

### 2. Activate Environment

This ensures your shell is correctly configured.

```bash
    conda activate venv
```

### 3. Start The Server

Once the environment is active, launch the `pygeoapi` server to expose your virtual datasets.

```bash
    ./bin/start-server.sh
```

## 📚 Retrieving Datasets

To avoid exceeding your storage quota, you'll to create a symlink as such:

```bash
    ln -s /fs/site5/eccc/mrd/rpnsi/$USER my_storage_space
```

Once that's done, you'll be able to run heavy scripts like `share/rpn-pygeoapi/fetch-data.py`.

This operation is necessary to retrieve public datasets like _ERA5_ from the web.

## 🐍 Using Conda (Preferred) vs Python Venv

Using `conda` is generally more reliable, especially when working with C-based dependencies like GDAL, as it avoids
common OS-level conflicts.

```bash
    # Ensures compatibility between GDAL and MapServer
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

## (Upcoming) Loading CONDA

What the lines look like in my bash default profile.

```bash
    # ~/.profile.d/default/post
    my-load-conda() {
        __conda_setup="$('/home/$USER/site5/miniconda3/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
        if [ $? -eq 0 ]; then
            eval "$__conda_setup"
        else
            if [ -f "/home/$USER/site5/miniconda3/etc/profile.d/conda.sh" ]; then
                . "/home/$USER/site5/miniconda3/etc/profile.d/conda.sh"
            else
                export PATH="/home/$USER/site5/miniconda3/bin:$PATH"
            fi
        fi
        unset __conda_setup
    }
```
