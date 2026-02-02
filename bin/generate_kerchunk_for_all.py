#!/usr/bin/env python3

import os
import glob
import ujson
import argparse
from kerchunk.combine import MultiZarrToZarr
from kerchunk.zarr import single_zarr

import time
from tqdm import tqdm
from datetime import datetime
from zoneinfo import ZoneInfo


import spinner

PARENT_DIR = 'zarr'
OUTPUT_DIR = 'combined_jsons'

def generate_index_for_subfamily(subfamily_path, output_path):
    """
    Generates a single Kerchunk JSON index for a specific subfamily subdirectory.
    
        Returns:
            - (True, None) on success,
            - (False, error_message) on failure.
    """
    
    if os.path.exists(output_path):
        return True, "Déjà existant (Skipped)"
    
    print(f"Processing: {subfamily_path}")
    
    zarr_files = sorted(glob.glob(os.path.join(subfamily_path, "*.zarr")))

    if not zarr_files:
        print(f"\t -> No .zarr found in {subfamily_path}, skipping.")
        return
    
    single_indexes = []
    
    for f in tqdm(zarr_files, desc=f"  -> Fichiers dans {os.path.basename(subfamily_path)}", leave=False):
        try:
            ds = single_zarr(
                f,
                inline_threshold=0
            )
            single_indexes.append(ds)
        except Exception as e:
            print(f"\t -> Error reading {f}: {e}.")
            continue
        
    if not single_indexes:
        print("\t -> No valid indexes generated.")
        return
    
    try:
        mzz = MultiZarrToZarr(
            single_indexes,
            remote_protocol='file',
            concat_dims=['time'],
            identical_dims=['lat', 'lon', 'height', 'y', 'x']
        )
        
        print(f"    Fusion de {len(single_indexes)} fichiers en cours...")
        #with Spinner("  Assemblage du JSON final "):
        dico_fusionne = mzz.translate()
            
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            ujson.dump(dico_fusionne, f)
            
        print(f"\t -> Success! Index saved to: {output_path}")
        
        return True, None
    
    except Exception as e:
        
        print(f"\t -> Error combining indexes for {subfamily_path}: {e}")
        return False, str(e)
    
def main():
    
    # --- Gestion des arguments ---
    parser = argparse.ArgumentParser(description="Généralise la création d'index Kerchunk pour des répertoires Zarr.")
    
    parser.add_argument(
        "-i", "--input",
        required=True,
        help="Répertoire parent contenant les dossiers de familles Zarr"
    )
    
    parser.add_argument(
        "-o", "--output",
        default="combined_jsons",
        help="Répertoire de sortie pour les fichiers JSON (défaut: combined_jsons)"
    )
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.input):
        print(f"Erreur : Le répertoire d'entrée '{args.input}' n'existe pas.")
        return
    
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    
    items = sorted(glob.glob(os.path.join(args.input, '*')))
    sub_folders = [i for i in items if os.path.isdir(i)]
    
    # --- CONFIGURATION DU TEMPS ---
    # On définit le timezone de Montréal
    mtl_tz = ZoneInfo("America/Montreal")
    
    start_dt = datetime.now(mtl_tz)
    print(f"Début du traitement de {len(sub_folders)} families Zarr...")
    print(f"Source : {args.input} | Destination : {args.output}")
    print(f"  - {start_dt.strftime('%Y-%m-%d %H:%M:%S')} (Montréal)")
    start_time = time.time()
    
    success_list = []
    failure_list = []
    
    for item in tqdm(sub_folders, desc="Progression globale", unit="famille"):
        
        folder_name = os.path.basename(item)
        output_json_path = os.path.join(args.output, f"{folder_name}.json")
            
        success, erreur_msg = generate_index_for_subfamily(item, output_json_path)
        
        if success:
            success_list.append(folder_name)
        else:
            failure_list.append((folder_name, erreur_msg))
    
    total_time = time.time() - start_time
    end_dt = datetime.now(mtl_tz)
    
    print(f"--- Terminé en {total_time:.2f} secondes ---")
    
    print("\n" + "="*50)
    print(f"RAPPORT DE TRAITEMENT (Durée : {total_time:.2f}s)")
    print("="*50)
    
    print(f"\n SUCCÈS : {len(success_list)} dossiers.")
    print(f"\n ÉCHECS : {len(failure_list)} dossiers.")
    
    for nom, erreur in failure_list:
        print(f"  - Dossier : {nom}")
        print(f"    Cause : {erreur}")
        print("-" * 30)
    
    print("\nFin du script.")
        
if __name__ == "__main__":
    main()
    
