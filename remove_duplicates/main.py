from pathlib import Path
from hashlib import md5
from argparse import ArgumentParser
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def group_entries_by_size(path: Path, recursive: bool = False) -> list[list[Path]]:
    files_by_size: dict[int, list[Path]] = {}
    
    iterator = path.rglob('*') if recursive else path.iterdir()
    
    for entry in iterator:
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

def search_duplicates(path: Path, recursive: bool = False) -> list[list[Path]]:
    entries = group_entries_by_size(path, recursive)
    
    if not entries:
        return []
        
    return [
        duplicate_lists 
        for entry in entries
        for duplicate_lists in entries_with_same_hash(entry)
        ]
        
    

def main(directory_path: Path, recursive: bool = False) -> None:
    
    if not directory_path.is_dir():
        logging.error(f"{directory_path} no es un directorio")
        return
    
    duplicates = search_duplicates(directory_path, recursive)
    
    if not duplicates:
        print("No se encontraron archivos duplicados")
        return
    
    print(f"Se encontraron {len(duplicates)} grupos de archivos duplicados:\n")
    
    for idx, duplicated_files in enumerate(duplicates, 1):
        size = duplicated_files[0].stat().st_size
        size_mb = size / (1024 * 1024)
        
        print(f"Grupo {idx} ({len(duplicated_files)} archivos, {size_mb:.2f} MB cada uno):")
        for file_idx, file in enumerate(duplicated_files, 1):
            print(f"  {file_idx}. {file}")
        print("")
    
    response = input("¿Deseas eliminar duplicados? (s/n): ").strip().lower()
    if response != 's':
        print("Operación cancelada")
        return
    
    for idx, duplicated_files in enumerate(duplicates, 1):
        print(f"\nGrupo {idx}:")
        for file_idx, file in enumerate(duplicated_files, 1):
            print(f"  {file_idx}. {file}")
        
        keep = input(f"¿Cuál archivo conservar? (1-{len(duplicated_files)}, 0=omitir, q=omitir todos): ").strip().lower()
        
        if keep == 'q':
            print("Omitiendo grupos restantes...")
            break
        
        if not keep.isdigit():
            print("Omitiendo grupo...")
            continue
            
        keep_idx = int(keep)
        if keep_idx == 0 or keep_idx > len(duplicated_files):
            print("Omitiendo grupo...")
            continue
        
        for file_idx, file in enumerate(duplicated_files, 1):
            if file_idx == keep_idx:
                print(f"  Conservando: {file}")
                continue
            try:
                file.unlink()
                print(f"  Eliminado: {file}")
            except Exception as e:
                logging.error(f"Error al eliminar {file}: {e}")
    
    print("\nProceso completado")
    
    
if __name__ == '__main__':
    parser = ArgumentParser(
        description='Busca y reporta archivos duplicados en un directorio'
    )
    
    parser.add_argument(
        'directory',
        type=Path,
        help='Ruta del directorio donde buscar archivos duplicados'
    )
    
    parser.add_argument(
        '-r', '--recursive',
        action='store_true',
        help='Buscar archivos duplicados recursivamente en subdirectorios'
    )
    
    args = parser.parse_args()
    
    main(args.directory, args.recursive)