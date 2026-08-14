import logging

import fsspec
import xarray as xr

import rmn.virtualizarr
from pygeoapi.provider.xarray_ import XarrayProvider


LOGGER = logging.getLogger(__name__)


class CustomXarrayProvider(XarrayProvider):

    def __init__(self, provider_def):

        rmn.virtualizarr.register_codec()

        self.data = provider_def["data"]

        # Manifest Kerchunk / VirtualiZarr
        if self.data.endswith(".json"):

            LOGGER.warning(
                "Opening Kerchunk manifest: %s",
                self.data
            )

            fs = fsspec.filesystem(
                "reference",
                fo=self.data,
            )

            mapper = fs.get_mapper("")

            self._data = xr.open_dataset(
                mapper,
                engine="zarr",
                consolidated=False,
            )

            LOGGER.warning(
                "Dataset opened successfully"
            )

            LOGGER.warning(
                "data_vars = %s",
                list(self._data.data_vars)
            )


            variables = [
                variable
                for variable in self._data.data_vars
                if not variable.startswith("record_")
            ]

            if not variables:
                raise RuntimeError(
                    "No scientific variable found in dataset"
                )

            LOGGER.warning(
                "Scientific variables: %s",
                variables
            )

            self._fields = {}

            first_da = None

            for variable_name in variables:

                da = self._data[variable_name]

                LOGGER.warning(
                    "Processing variable: %s",
                    variable_name
                )

                LOGGER.warning(
                    "Variable dimensions: %s",
                    da.dims
                )

                LOGGER.warning(
                    "Variable shape: %s",
                    da.shape
                )

                if len(da.dims) < 2:
                    LOGGER.warning(
                        "Skipping variable %s: not enough dimensions",
                        variable_name
                    )
                    continue

                x_field = da.dims[0]
                y_field = da.dims[1]

                LOGGER.warning(
                    "%s: x_field=%s y_field=%s",
                    variable_name,
                    x_field,
                    y_field
                )

                coordinates = {
                    x_field: range(
                        da.sizes[x_field]
                    ),
                    y_field: range(
                        da.sizes[y_field]
                    ),
                }

                da = da.assign_coords(coordinates)

                self._data[variable_name] = da

                LOGGER.warning(
                    "%s: Coordinates created: %s",
                    variable_name,
                    list(da.coords)
                )


                if first_da is None:
                    first_da = da
                    self.variable = variable_name
                    self.x_field = x_field
                    self.y_field = y_field

                self._fields[variable_name] = {
                    "type": "float",
                    "x-ogc-unit": "1"
                }

            if first_da is None:
                raise RuntimeError(
                    "No valid scientific variable found in dataset"
                )


            self.time_field = None
            self.storage_crs = None

            shape = first_da.shape

            self._coverage_properties = {
                "width": shape[0],
                "height": shape[1],
                "depth": shape[2] if len(shape) > 2 else 1,

                "resx": 1.0,
                "resy": 1.0,

                "crs_type": "GeographicCRS",
                "bbox_crs": (
                    "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
                ),

                "axes": {
                    "x": {
                        "key": self.x_field
                    },
                    "y": {
                        "key": self.y_field
                    }
                }
            }

            self.axes = self._coverage_properties["axes"]

            LOGGER.warning(
                "Coverage properties = %s",
                self._coverage_properties
            )

            LOGGER.warning(
                "Fields initialized: %s",
                self._fields
            )

        else:
            super().__init__(provider_def)
