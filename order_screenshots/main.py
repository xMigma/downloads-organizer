from pathlib import Path
from datetime import datetime
import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

DEFAULT_SCREENSHOTS_DIR = "/home/miguel/Imágenes/Capturas de Pantalla"

def move_file_to_date_folder(directory: Path):
    for file in directory.iterdir():
        if not file.is_file():
            logging.debug(f"Omitiendo (no es archivo): {file.name}")
            continue
        
        stat = file.stat()
        date = datetime.fromtimestamp(stat.st_mtime)
        
        year_iso, week, _ = date.isocalendar()
        date_dir = directory / f"{year_iso}_sem{week:02d}"
        
        date_dir.mkdir(exist_ok=True)
        logging.info(f"Mover '{file.name}' a '{date_dir}'")
        file.rename(date_dir / file.name)
        logging.info(f"Archivo '{file.name}' movido correctamente.")

def main():
    if len(sys.argv) > 1:
        directory = Path(sys.argv[1])
    else:
        directory = Path(DEFAULT_SCREENSHOTS_DIR)
        logging.info(f"No se proporcionó directorio, usando default: {directory}")
    
    if not directory.is_dir():
        logging.error(f"{directory} no es un directorio")
        return
    
    move_file_to_date_folder(directory)


if __name__ == '__main__':
    main()