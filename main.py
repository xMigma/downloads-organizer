import logging
import sys

from file_organizer import order_dir

DIR_PATH = "/home/miguel/Descargas"

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        order_dir(DIR_PATH)
        
    except (FileNotFoundError, NotADirectoryError) as e:
        logger.error(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Error inesperado: {e}")
        sys.exit(1)

