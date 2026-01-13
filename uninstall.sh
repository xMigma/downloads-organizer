#!/bin/bash

echo "Desinstalando organizador de descargas..."
echo ""

INSTALL_PATH="${INSTALL_DIR:-$HOME/.local/bin/file-organizer}"

# Eliminar cron job
if crontab -l 2>/dev/null | grep -q "$INSTALL_PATH/main.py"; then
    echo "Eliminando cron job..."
    crontab -l | grep -v "$INSTALL_PATH/main.py" | crontab -
    echo "Cron job eliminado"
else
    echo "No se encontro cron job instalado"
fi

# Eliminar archivos
if [ -d "$INSTALL_PATH" ]; then
    echo "Eliminando archivos de $INSTALL_PATH..."
    rm -rf "$INSTALL_PATH"
    echo "Archivos eliminados"
else
    echo "No se encontraron archivos instalados"
fi

echo ""
echo "Desinstalacion completada!"
