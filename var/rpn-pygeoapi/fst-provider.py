import logging

from pygeoapi.provider.base import (BaseProvider)
LOGGER = logging.getLogger(__name__)

class FstProvider(BaseProvider):
    def __init__(self, provider_def):
        super().__init__(provider_def)
        LOGGER.debug('Detected multi file dataset')

        if  provider_def['data'].endswith('.fst'):
            # open_func = 
            print("Bonjour")
    
    def get_fields(self):
        return {}

    def query(self, properties=[], subsets={}, bbox=[], bbox_crs=4326,
              datetime_=None, format_='json', **kwargs):
        return {}
