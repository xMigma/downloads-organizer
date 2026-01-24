from pathlib import Path
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

SCREENSHOTS_DIR = "/home/miguel/Imágenes/Prueba"

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
    directory = Path(SCREENSHOTS_DIR)
    
    if not directory.is_dir():
        logging.error(f"{directory} no es un directorio")
        return
    
    move_file_to_date_folder(directory)
    
    
if __name__ == '__main__':
    main()