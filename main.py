import logging
import sys
import argparse
from pathlib import Path

from file_organizer import order_dir

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

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

