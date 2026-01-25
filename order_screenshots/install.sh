#!/bin/bash
set -e

# Obtener directorio del script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SHARED_DIR="$(dirname "$SCRIPT_DIR")/shared"

# Cargar librería compartida
source "$SHARED_DIR/cron_installer.sh"

# Configuración específica de este organizador
CRON_ID="screenshot-organizer"
APP_NAME="Organizador de Screenshots"
DEFAULT_INSTALL_PATH="$HOME/.local/bin/screenshot-organizer"
FILES_TO_INSTALL="main.py"

show_install_banner "$APP_NAME"

# Detectar directorio de instalación
INSTALL_PATH="${INSTALL_DIR:-$DEFAULT_INSTALL_PATH}"

# Instalar archivos
install_files "$INSTALL_PATH" "$FILES_TO_INSTALL"
chmod +x "$INSTALL_PATH/main.py"

echo "Archivos instalados en: $INSTALL_PATH"
echo ""

# Preguntar directorio a organizar
DEFAULT_DIR="$HOME/Imágenes/Capturas de Pantalla"
if [ ! -d "$DEFAULT_DIR" ]; then
    DEFAULT_DIR="$HOME/Pictures/Screenshots"
fi

TARGET_DIR=$(ask_directory "¿Qué directorio de screenshots quieres organizar?" "$DEFAULT_DIR")

# Verificar directorio
if ! ensure_directory "$TARGET_DIR"; then
    echo "Instalación cancelada."
    exit 1
fi

# Configurar cron job
echo ""
echo "Configurando cron job para ejecutar al inicio..."

LOG_FILE="$INSTALL_PATH/organizer.log"
COMMAND="python3 $INSTALL_PATH/main.py \"$TARGET_DIR\""

install_reboot_cron "$CRON_ID" "$COMMAND" "$LOG_FILE"

show_install_complete "$TARGET_DIR" "$LOG_FILE" "$INSTALL_PATH" "$COMMAND"
