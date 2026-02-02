from warnings import resetwarnings
from pygeoapi.provider.xarray_ import XarrayProvider
import numpy as np
import logging
import xarray as xr

LOGGER = logging.getLogger(__name__)
class CustomXarrayProvider(XarrayProvider):
    
    def __init__(self, provider_def): 
        # On ne peut pas appeler super().__init__ directement car il échouerait
        # à ouvrir le JSON comme un dataset classique. 
        # Il faut reproduire une partie de la logique de xarray_.py
        
        self.data = provider_def['data']
        if self.data.endswith('.json'): 
            #Logique Kerchunk 
            fs = fsspec.filesystem("reference", fo=self.data, remote_options={'anon': True}) # à adapter
            
            m = fs.get_mapper("") 
            self._data = xr.open_dataset(m, engine="zarr", consolidated=False) 
            
            # Initialisation des propriétés requises par pygeoapi 
            self.storage_crs = self._parse_storage_crs() 
            self._coverage_properties = self._get_coverage_properties() 
            self.axes = self._coverage_properties['axes'] 
            self.get_fields()
        else: 
            super().__init__(provider_def)
    """
    This wrapper class serves as a custom Xarray Provider
    """
    def _sanitize(self, obj):
        """Clean lists and dictionaries recursively"""
        if  isinstance(obj, dict):
            return {k: self._sanitize(v) for k, v in obj.items()}
        elif  isinstance(obj, list):
            return [self._sanitize(v) for v in obj]
        
        if isinstance(obj, (bytes, np.bytes_)):
            return obj.decode('utf-8', errors='ignore')
        if isinstance(obj, (np.dtype, type(np.dtypes.BytesDType))):
            return str(obj)
        if isinstance(obj, np.generic):
            return obj.item()        
        return obj
    
    def gen_covjson(self, metadata, data, fields):
        """
        Generate coverage as CoverageJSON representation

        :param metadata: coverage metadata
        :param data: rasterio DatasetReader object
        :param fields: fields

        :returns: dict of CoverageJSON representation
        """

        LOGGER.debug('Creating CoverageJSON domain')
        minx, miny, maxx, maxy = metadata['bbox']

        selected_fields = {
            key: value for key, value in self.fields.items()
            if key in fields
        }

        try:
            tmp_min = data.coords[self.y_field].values[0]
        except IndexError:
            tmp_min = data.coords[self.y_field].values
        try:
            tmp_max = data.coords[self.y_field].values[-1]
        except IndexError:
            tmp_max = data.coords[self.y_field].values

        if tmp_min > tmp_max:
            LOGGER.debug(f'Reversing direction of {self.y_field}')
            miny = tmp_max
            maxy = tmp_min

        cj = {
            'type': 'Coverage',
            'domain': {
                'type': 'Domain',
                'domainType': 'Grid',
                'axes': {
                    'x': {
                        'start': minx,
                        'stop': maxx,
                        'num': metadata['width']
                    },
                    'y': {
                        'start': maxy,
                        'stop': miny,
                        'num': metadata['height']
                    }
                },
                'referencing': [{
                    'coordinates': ['x', 'y'],
                    'system': {
                        'type': self._coverage_properties['crs_type'],
                        'id': self._coverage_properties['bbox_crs']
                    }
                }]
            },
            'parameters': {},
            'ranges': {}
        }

        if (data.coords[self.x_field].size == 1 and
                data.coords[self.y_field].size == 1):
            LOGGER.debug('Modelling as PointSeries')
            cj['domain']['axes']['x'] = {
                'values': [float(data.coords[self.x_field].values)]
            }
            cj['domain']['axes']['y'] = {
                'values': [float(data.coords[self.y_field].values)]
            }
            cj['domain']['domainType'] = 'PointSeries'

        if self.time_field is not None:
            LOGGER.debug('Adding time axis')
            cj['domain']['axes']['t'] = {
                'values': [str(v) for v in (
                    data[self.time_field].values
                    if hasattr(data[self.time_field].values, '__iter__')
                    else [data[self.time_field].values]
                    )
                ]
            }
            cj['domain']['referencing'].append({
                'coordinates': ['t'],
                'system': {
                    'type': 'TemporalRS',
                    'calendar': 'Gregorian'
                }
            })

        LOGGER.debug('Adding parameters')
        for key, value in selected_fields.items():
            parameter = {
                'type': 'Parameter',
                'description': {
                    'en': value['title']
                },
                'unit': {
                    'symbol': value['x-ogc-unit']
                },
                'observedProperty': {
                    'id': key,
                    'label': {
                        'en': value['title']
                    }
                }
            }

            cj['parameters'][key] = parameter

        data = data.fillna(None)

        try:
            for key, value in selected_fields.items():
                LOGGER.debug(f'Adding range {key}')
                cj['ranges'][key] = {
                    'type': 'NdArray',
                    'dataType': value['type'],
                    'axisNames': [
                        'y', 'x'
                    ],
                    'shape': [metadata['height'],
                              metadata['width']]
                }
                cj['ranges'][key]['values'] = [
                    None if np.isnan(v) else v
                    for v in data[key].values.flatten()
                ]

                if self.time_field is not None:
                    cj['ranges'][key]['axisNames'].append('t')
                    cj['ranges'][key]['shape'].append(metadata['time_steps'])
        except IndexError as err:
            LOGGER.warning(err)
            raise ProviderQueryError('Invalid query parameter')

        LOGGER.debug('Returning data')
        return cj
    
    def get_fields(self):
        fields = super().get_fields()
        
        
        LOGGER.debug("FIELDS GETTER")
        clean_fields = self._sanitize(fields)
        self._fields = clean_fields
        
        return clean_fields
    
    def get_schema(self, **kwargs):
        LOGGER.debug("BONJOUR")
        schema = super().get_schema(**kwargs)
        return self._sanitize(schema)
    
    def get_metadata(self):
        
        LOGGER.debug("SALUT J'EXISSTEEE")
        metadata = super().get_metadata()
        
        return self._sanitize(metadata)
