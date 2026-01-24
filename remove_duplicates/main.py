from pathlib import Path
from hashlib import md5
from argparse import ArgumentParser
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def group_entries_by_size(path: Path) -> list[list[Path]]:
    files_by_size: dict[int, list[Path]] = {}
    
    for entry in path.iterdir():
        if entry.is_dir():
            logging.debug(f'Skipping directory: {entry}')
            continue
        
        size = entry.stat().st_size
        files_by_size.setdefault(size, []).append(entry)
    
    return [
    file_list
    for file_list in files_by_size.values()
    if len(file_list) > 1
    ]
    
def entries_with_same_hash(paths: list[Path]) -> list[list[Path]]:
    hash_duplicates: dict[str, list[Path]] = {}
    
    for path in paths:
        hash = md5(path.read_bytes()).hexdigest()
        hash_duplicates.setdefault(hash, []).append(path)
    
    return [
    file_list
    for file_list in hash_duplicates.values()
    if len(file_list) > 1
    ]

def search_duplicates(path: Path) -> list[list[Path]]:
    entries = group_entries_by_size(path)
    
    if not entries:
        return []
        
    return [
        duplicate_lists 
        for entry in entries
        for duplicate_lists in entries_with_same_hash(entry)
        ]
        
    

def main(directory_path: Path) -> None:
    
    if not directory_path.is_dir():
        logging.error(f"{directory_path} no es un directorio")
        return
    
    duplicates = search_duplicates(directory_path)
    
    if not duplicates:
        print("No se encontraron archivos duplicados")
        return
    
    print(f"Se encontraron {len(duplicates)} grupos de archivos duplicados:\n")
    
    for idx, duplicated_files in enumerate(duplicates, 1):
        size = duplicated_files[0].stat().st_size
        size_mb = size / (1024 * 1024)
        
        print(f"Grupo {idx} ({len(duplicated_files)} archivos, {size_mb:.2f} MB cada uno):")
        for file in duplicated_files:
            print(f" - {file}")
        print("")
    
    
if __name__ == '__main__':
    parser = ArgumentParser(
        description='Busca y reporta archivos duplicados en un directorio'
    )
    
    parser.add_argument(
        'directory',
        type=Path,
        help='Ruta del directorio donde buscar archivos duplicados'
    )
    
    args = parser.parse_args()
    
    main(args.directory)