# Requêtes pygeoapi de coverage

## 1. Le format des dates et temps

Il arrive que les requêtes se cassent ici. Voici quelques pistes de réflexions et "hacks" qui fonctionnent:

    - **L'astuce de l'étendue:** Si une date seule (2022-01-01) fait planter l'API
Ce fichier documente les différentes requêtes pour récupérer des données via pygeoapi OGC Coverage API.

## Le "Cheat Sheet" des URLs Coverage

| Cas de figure | Structure de l'URL | Astuce |
|:--|:--|:--|
| Cas de base | `/coverage?f=json` | __Attention:__ le dataset peut être trop volumineux pour être chargé en une seule fois. Utiliser plutôt des tranches spatiales ou temporales `bbox`, `datetime`, ou `subset` |
| Date unique | `/coverage?f=json&datetime=YYYY-MM-JJT00:00:00Z` |:--|
| Précision de l'heure | `/coverage?f=json` |:--|
| Plage de temps | `/coverage?f=json&datetime=YYYY-MM-JJT00:00:00Z/YYYY-MM-JJT00:00:00Z` |:--|
| Spécifier le format | `/coverage?f=zarr` |:--|
| Problème de CRS | `/coverage?f=json` |:--|

## Test & Debugging 

### ERA5

1. http://localhost:5000/collections/public-zarr/coverage?f=zarr


```python
TypeError

TypeError: Expected a BytesBytesCodec. Got <class 'numcodecs.blosc.Blosc'> instead.
```

### Zarr (gdps-weong)

1. http://localhost:5000/collections/local-zarr/coverage?f=zarr

```
DTypePromotionError

numpy.exceptions.DTypePromotionError: The DType <class 'numpy.dtypes.StrDType'> could not be promoted by <class 'numpy.dtypes._PyFloatDType'>. This means that no common DType exists for the given inputs. For example they cannot be stored in a single array unless the dtype is `object`. The full list of DTypes is: (<class 'numpy.dtypes.StrDType'>, <class 'numpy.dtypes._PyFloatDType'>)
Raised while encoding variable 'WindDir' with value <xarray.Variable (time: 308, lat: 1251, lon: 1801)> Size: 3GB
[693939708 values with dtype=float32]
Attributes: (12/14)
    long_name:        Meteorological wind direction
    units:            degree
    standard_name:    WindDir
    grid_mapping:     latitude_longitude_grid
    cell_methods:     time: point
    valid_min:        0.0
    ...               ...
    nomvar:           WD
    codes:            
    level:            1.0
    available_times:  ['2026-01-29T01:00', '2026-01-29T02:00', '2026-01-29T03...
    cumul_method:     ip2_minus_ip3
    coordinates:      time lat lon

```
