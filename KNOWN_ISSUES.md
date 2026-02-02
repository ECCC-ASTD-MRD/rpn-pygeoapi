# Known Issues

## Sérialisation JSON des données Xarray

**Status:** Non résolu

**Description:** Le sérialisateur JSON par défaut de Pygeoapi ne gère pas les types binaires NumPy (ex: `|S1`) ou les `BytesDType` générés par certains fichiers Zarr/NetCDF.

**Impact:** L'endpoint `/schema?f=json` retourne une page d'erreur pour certaines collections. Le HTML fonctionne (`/schema?f=html`)

**Piste de solution:** Voir le CustomProvider ou nettoyer les données sources.

**Dataset utilisé:** `zarr/caps-wings/20260119T00Z_MSC_CAPS-WEonG_AllVar-WINGS_Sfc_RLatLon0.03.zarr`
            
