# File Automation Toolkit

Conjunto de scripts de Python para automatizar la organización de archivos y eliminación de duplicados.

## Herramientas

| Script | Función |
|--------|---------|
| `order_downloads` | Clasifica archivos por extensión (Imágenes, Docs, Videos...) |
| `order_screenshots` | Organiza capturas por semana (`2024_sem05`) |
| `remove_duplicates` | Detecta y elimina archivos duplicados (hash MD5) |

## Instalación Rápida

```bash
# Descargas
./order_downloads/install.sh

# Capturas
./order_screenshots/install.sh
```

Los scripts se ejecutan automáticamente en cada reinicio (`@reboot` vía cron).

## Uso Manual

```bash
# Organizar descargas
python3 order_downloads/main.py ~/Downloads

# Organizar capturas
python3 order_screenshots/main.py

# Buscar duplicados (recursivo)
python3 remove_duplicates/main.py ~/Downloads -r
```

## Personalización

Edita `order_downloads/extensions.json` para añadir o modificar categorías de archivos.

## Desinstalación

```bash
./order_downloads/uninstall.sh
./order_screenshots/uninstall.sh
```

## Requisitos

- Python 3.8+
- Linux/macOS con cron
