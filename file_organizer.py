from pathlib import Path
import logging

from extensions import EXTENSIONS_DICT

logger = logging.getLogger(__name__)

def move_file(path: Path, file: Path):
    """Mueve un archivo a su carpeta correspondiente según su extensión."""
    file_ext = file.suffix.lower()

    moved = False
    for folder, extensions in EXTENSIONS_DICT.items():
        # Verificar si la extensión del archivo está en el conjunto de extensiones
        if file_ext in extensions:
            new_path = path / folder
            new_path.mkdir(exist_ok=True)
            logger.info(f"Moviendo '{file.name}' -> {folder}/")
            file.rename(new_path / file.name)
            moved = True

    # Si la extensión no coincide con ninguna categoría se mueve a "others"
    if not moved:
        logger.warning(f"Extensión no reconocida: {file.name} ({file_ext})")
        new_path = path / "others"
        new_path.mkdir(exist_ok=True)
        logger.info(f"Moviendo '{file.name}' -> others/")
        file.rename(new_path / file.name)


def order_dir(dir_path: str):
    """Organiza todos los archivos existentes en un directorio."""
    path = Path(dir_path)

    logger.info(f"Iniciando organización de archivos en: {dir_path}")
    if not path.exists():
        raise FileNotFoundError(f"La ruta '{dir_path}' no existe.")

    if not path.is_dir():
        raise NotADirectoryError(f"La ruta '{dir_path}' no es un directorio")

    files_moved = 0
    for file in path.iterdir():
        if not file.is_file():
            logger.debug(f"Omitiendo (no es archivo): {file.name}")
            continue

        move_file(path, file)
        files_moved += 1

    logger.info(f"Organización completada: {files_moved} archivos movidos")
