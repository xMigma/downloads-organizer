from pathlib import Path
import logging
import sys

from extensions import EXTENSIONS_DICT

DIR_PATH = "/home/miguel/Descargas"

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def main():
    path = Path(DIR_PATH)

    logger.info(f"Iniciando organización de archivos en: {DIR_PATH}")

    if not path.exists():
        raise FileNotFoundError(f"La ruta '{DIR_PATH}' no existe.")

    if not path.is_dir():
        raise NotADirectoryError(f"La ruta '{DIR_PATH}' no es un directorio")

    files_moved = 0

    for file in path.iterdir():
        if not file.is_file():
            logger.debug(f"Omitiendo (no es archivo): {file.name}")
            continue

        file_ext = file.suffix.lower()

        moved = False
        for folder, extensions in EXTENSIONS_DICT.items():
            if file_ext in extensions:
                new_path = path / folder
                new_path.mkdir(exist_ok=True)
                logger.info(f"Moviendo '{file.name}' -> {folder}/")
                file.rename(new_path / file.name)
                files_moved += 1
                moved = True
                break

        if not moved:
            logger.warning(f"Extensión no reconocida: {file.name} ({file_ext})")
            new_path = path / "others"
            new_path.mkdir(exist_ok=True)
            logger.info(f"Moviendo '{file.name}' -> others/")
            file.rename(new_path / file.name)
            files_moved += 1

    logger.info(f"Organización completada: {files_moved} archivos movidos")
        

if __name__ == "__main__":
    try:
        main()
    except (FileNotFoundError, NotADirectoryError) as e:
        logger.error(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Error inesperado: {e}")
        sys.exit(1)

