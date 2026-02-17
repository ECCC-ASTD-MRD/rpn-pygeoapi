#!/usr/bin/env python3

import pathlib
import argparse

import zoneinfo
import datetime
import time

from kerchunk.combine import MultiZarrToZarr
from kerchunk.zarr import single_zarr

import ujson # ultra fast JSON encoder and decoder written in pure C
from tqdm import tqdm

DESCRIPTION = "Généralise la création d'index Kerchunk pour des répertoires Zarr."

def get_args():
    
    p = argparse.ArgumentParser(description=DESCRIPTION)
    
    p.add_argument(
        "-i", "--input",
        required=True,
        type=pathlib.Path,
        help="Répertoire parent contenant les dossiers de familles Zarr"
    )
    
    p.add_argument(
        "-o", "--output",
        default="data/combined_jsons",
        type=pathlib.Path,
        help="Répertoire de sortie pour les fichiers JSON (défaut: combined_jsons)"
    )
    
    args = p.parse_args()
    
    if not args.input.is_dir():
        p.error(f"Erreur : Le répertoire d'entrée '{args.input}' n'existe pas.")
        
    return args

def main():
    
    args = get_args()
    
    args.output.mkdir(parents=True, exist_ok=True)
    
    # Sets Montreal Timezone for DEBUG log
    mtl_tz = zoneinfo.ZoneInfo("America/Montreal")
    start_dt = datetime.datetime.now(mtl_tz)
    
    input_path = args.input
    output_dir = args.output
    
    print(f"Source : {input_path.resolve()} | Destination : {output_dir.resolve()}")
    print(f"  - {start_dt.strftime('%Y-%m-%d %H:%M:%S')} (Montreal)")
    
    start_time = time.perf_counter()
    
    sub_folders = sorted([f for f in input_path.iterdir() if f.is_dir()])
    
    success_list = []
    failure_list = []
    
    for folder in tqdm(sub_folders, desc="Overall Progress", unit="family"):
        
        json_file = output_dir / f"{folder.name}.json"
        
        success, error_msg = generate_index(folder, json_file)
        
        if success:
            success_list.append(folder.name)
        else:
            failure_list.append((folder.name, error_msg))
    
    end_time = time.perf_counter()
    total_time = end_time - start_time
    
    end_dt = datetime.datetime.now(mtl_tz)
    
    print(f"--- Terminé en {total_time:.2f} secondes ---")
    
    print("\n" + "="*50)
    print(f"RAPPORT DE TRAITEMENT (Durée : {total_time:.2f}s)")
    print("="*50)
    
    print(f"\n SUCCÈS : {len(success_list)} dossiers.")
    print(f"\n ÉCHECS : {len(failure_list)} dossiers.")
    
    for name, error in failure_list:
        print(f"  - Dossier : {name}")
        print(f"    Cause : {error}")
        print("-" * 30)
    
    print("\nEnd of script.")
    
    
def generate_index(input_dir, output_dir):
    '''
        Parameters:
            - input_dir: Folder containing the Zarr files to merge
            - output_dir: Folder in which the JSON manifest is created
    '''
    zarr_files = sorted(list(input_dir.glob("*.zarr")))

    single_indexes = []

    for f in tqdm(zarr_files, desc=f"  -> Files in {input_dir.name}", leave=False):
        try:
            ds = single_zarr(str(f), inline_threshold=0)
            single_indexes.append(ds)
        except Exception as e:
            print(f"\t -> Error reading {f.name}: {e}.")
            return False, "${e}"# raise e
    
    if not single_indexes:
        return False, "Aucun index créé."

    try:
        mzz = MultiZarrToZarr(
            single_indexes,
            remote_protocol='file',
            concat_dims=['time'],
            identical_dims=['lat', 'lon']
        )
        
        print(f"    Fusion de {len(single_indexes)} fichiers en cours...")
        dico_fusionne = mzz.translate()
            
        output_dir.parent.mkdir(parents=True, exist_ok=True)
        output_dir.write_text(ujson.dumps(dico_fusionne))

        return True, "Succès"
    except Exception as e:
        print(f"\t -> Error combining indexes for {input_dir}: {e}")
        return False, f"{e}"
    
        
if __name__ == "__main__":
    main()
