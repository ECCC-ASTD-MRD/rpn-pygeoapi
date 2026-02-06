# Single Kerchunk Index (manuel/prototype)

Ce script est la version brouillon du générateur d'index Kerchunk. Il est utile pour tester et déboguer l'index d'une famille très spécifique qui poserait problème. 

**Important:** Ce script ne prend **aucun argument** en ligne de commande. Vous devez éditer les variables directement dans le fichier `.py`

## Configuration

Ouvrez `bin/generate_kerchunk.py` et modifiez les constantes en haut du fichier :

```python
    ZARR_DIR = 'zarr/caps-wings'            # <-- Le dossier spécifique à traiter
    OUTPUT_JSON = './combined.json'         # <-- Le nom du fichier de sortie
```

## Usage 

Une fois les variables modifiées et sauvegardées:
```bash
    python bin/generate_kerchunk.py
```

