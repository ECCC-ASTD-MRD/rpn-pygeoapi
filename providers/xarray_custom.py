import logging
import fsspec
import xarray as xr

from pygeoapi.provider.xarray_ import XarrayProvider

LOGGER = logging.getLogger(__name__)


class CustomXarrayProvider(XarrayProvider):
    def __init__(self, provider_def):
        super().__init__(provider_def)

        self.data = provider_def["data"]

        if self.data.endswith(".json"):
            LOGGER.debug(
                f"Opening Kerchunk manifest: {self.data}"
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

            self.storage_crs = self._parse_storage_crs()
            self._coverage_properties = self._get_coverage_properties()
            self.axes = self._coverage_properties["axes"]

            self.get_fields()

        else:
            super().__init__(provider_def)
