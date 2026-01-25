#!/bin/bash

# Obtener directorio del script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SHARED_DIR="$(dirname "$SCRIPT_DIR")/shared"

# Cargar librería compartida
source "$SHARED_DIR/cron_installer.sh"

# Configuración específica
CRON_ID="screenshot-organizer"
DEFAULT_INSTALL_PATH="$HOME/.local/bin/screenshot-organizer"

echo "Desinstalando organizador de screenshots..."
echo ""

INSTALL_PATH="${INSTALL_DIR:-$DEFAULT_INSTALL_PATH}"

# Eliminar cron job
remove_cron_by_id "$CRON_ID"

# Eliminar archivos
if [ -d "$INSTALL_PATH" ]; then
    echo "Eliminando archivos de $INSTALL_PATH..."
    rm -rf "$INSTALL_PATH"
    echo "Archivos eliminados"
else
    echo "No se encontraron archivos instalados"
fi

echo ""
echo "Desinstalación completada!"
