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

            LOGGER.warning("Dataset opened successfully")

            LOGGER.warning(
                "data_vars = %s",
                list(self._data.data_vars)[:20]
            )


            #
            # Sélection automatique d'une variable 
            #

            variables = [
                v
                for v in self._data.data_vars
                if not v.startswith("record")
            ]

            if not variables:
                raise RuntimeError(
                    "No scientific variable found in dataset"
                )


            self.variable = variables[0]

            LOGGER.warning(
                "Selected variable: %s",
                self.variable
            )


            da = self._data[self.variable]

            LOGGER.warning(
                "Variable dimensions: %s",
                da.dims
            )


            #
            # Détection  des axes
            #

            if len(da.dims) < 2:
                raise RuntimeError(
                    "Variable does not have enough dimensions"
                )


            self.x_field = da.dims[0]
            self.y_field = da.dims[1]


            LOGGER.warning(
                "x_field=%s y_field=%s",
                self.x_field,
                self.y_field
            )


            #
            # Attributs attendus par XarrayProvider
            #

            self.time_field = None

            self.storage_crs = None

            shape = da.shape

           
            self._coverage_properties = {
                "width": shape[0],
                "height": shape[1],
                "depth": shape[2] if len(shape) > 2 else 1,

                
                "resx": 1.0,
                "resy": 1.0,

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


            

            self._fields = {
                self.variable: {
                    "type": "float"
                }
            }


            LOGGER.warning(
                "Fields initialized: %s",
                self._fields
            )


        else:
            super().__init__(provider_def)
