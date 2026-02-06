# Requêtes pygeoapi de coverage

## 1. Le format des dates et temps

Il arrive que les requêtes se cassent ici. Voici quelques pistes de réflexions et "hacks" qui fonctionnent:

    - **L'astuce de l'étendue:** Si une date seule (2022-01-01) fait planter l'API
Ce fichier documente les différentes requêtes pour récupérer des données via pygeoapi OGC Coverage API.

## Le "Cheat Sheet" des URLs Coverage

| Cas de figure | Structure de l'URL | Astuce |
|:--|:--|:--|
| Date unique | `/coverage?f=json` |:--|
| Précision de l'heure | `/coverage?f=json` |:--|
| Plage de temps | `/coverage?f=json` |:--|
| Spécifier le format | `/coverage?f=zarr` |:--|
| Problème de CRS | `/coverage?f=json` |:--|

