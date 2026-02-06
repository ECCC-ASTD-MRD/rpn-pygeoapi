# Générateur de manifeste JSON avec Kerchunk

## Rôle du script

Ce script automatise la création de fichiers JSON (Kerchunk) pour des répertoires de données Zarr.

Concrètement, il parcourt un dossier parent contenant plusieurs sous-dossiers (familles de données). Pour chaque famille, il combine tous les fichiers `.zarr` individuels (souvent segmentés par pas de temps) en un seul fichier JSON virtuel.

Cela permet à `xarray` d'ouvrir une série temporelle complète instantanément.

## Structure attendue

Le script s'attend à une structure d'entrée hiérarchique:

```
input_directory/            <-- Ce que vous passez en argument -i
├── famille_A/              <-- Sera traité comme un dataset unique
    ├── T00.zarr
    ├── T01.zarr
├── famille_B/
    ├── ...
```

## Utilisation

Depuis la racine du projet (`rpn-pygeoapi`), lancez la commande suivante:

```bash
    python bin/generate_kerchunk_for_all.py -i <dossier_source> -o <dossier_sortie>
```

### Paramètres

| Argument | Flag court | Description | Exemple |
|:---------|:-----------|:------------|:--------|
| Input    | `-i`       | Chemin vers le dossier parent contenant les sous-dossiers de familles Zarr | `zarr` (ou le lien symbolique) |
| Output    | `-o`       | Dossier où les fichiers JSON combinés seront sauvegardés. (Défaut: `combined_jsons`) | `combined_jsons/` |

### Exemple

Pour regénérer les index basés sur le lien symbolique `zarr` présent à la racine et mettre à jour le dossier `combined_jsons` existant:

```bash
    python bin/generate_kerchunk_for_all.py -i zarr -o combined_jsons
```

Cela générera des fichiers comme `combined_jsons/hrdps-wings.json`, `combined_jsons/geps-weong.json`, etc.
