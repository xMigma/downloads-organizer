import logging
import sys
import argparse
import json
from pathlib import Path

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def _load_extensions():
    """Carga las extensiones desde el archivo JSON de configuración."""
    config_path = Path(__file__).parent / "extensions.json"
    with open(config_path, 'r', encoding='utf-8') as f:
        extensions_dict = json.load(f)
    # Convertir listas a sets para búsqueda más eficiente
    return {category: set(exts) for category, exts in extensions_dict.items()}


def move_file(path: Path, file: Path, extensions_dict: dict):
    """Mueve un archivo a su carpeta correspondiente según su extensión."""
    file_ext = file.suffix.lower()

    moved = False
    for folder, extensions in extensions_dict.items():
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
    extensions_dict = _load_extensions()
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

        move_file(path, file, extensions_dict)
        files_moved += 1

    logger.info(f"Organización completada: {files_moved} archivos movidos")

if __name__ == "__main__":
    # Parsear argumentos de línea de comandos
    parser = argparse.ArgumentParser(
        description="Organiza archivos en carpetas según su extensión"
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=str(Path.home() / "Downloads"),
        help="Directorio a organizar (por defecto: ~/Downloads)"
    )
    args = parser.parse_args()

    try:
        order_dir(args.directory)
    except (FileNotFoundError, NotADirectoryError) as e:
        logger.error(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Error inesperado: {e}")
        sys.exit(1)

